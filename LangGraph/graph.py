from json import load
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from openai import OpenAI
from pydantic import BaseModel

#Schema 
class DetectCallResponse(BaseModel):
    is_question_ai : bool

class CoodingAIResponse(BaseModel):
    answer : str

# Load environment variables
client = wrap_openai(OpenAI())
load_dotenv()


# Define the state
class State(TypedDict):
    user_message:str
    ai_message:str
    is_coding_question:bool

# This is a simple state graph example
def detect_query(state:State):
    user_message = state.get("user_message")

#openai api call (gpt-4o-mini)
    SYSTEM_PROMPT = """
You are an AI assistant. Your job is to detect if the user's query is related to coding question or not.
Return the response in specified JSON boolean only.
    """

    #openai api call 
    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=DetectCallResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        
            ],
        
    )
    # print(result.choices[0].message.parsed.is_question_ai)
    state["is_coding_question"] = result.choices[0].message.parsed.is_question_ai
    return state

def route_edge(state:State) ->Literal["solve_coding_question", "solve_simple_question"]:
    is_coding_question =  state.get("is_coding_question")
    if is_coding_question:
        return "solve_coding_question"
    else:
        return "solve_simple_question"

#solve_coding_question function
def solve_coding_question(state:State):
    user_message = state.get("user_message")

    #openai api call ( cooding question gpt-4.1)
    SYSTEM_PROMPT = """
You are an AI assistant. Your job is to resolve the user query based on coding problem he is facing.
    """

    #openai api call 
    result = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=CoodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        
            ],
            max_tokens=200

        
    )
     # state["ai_message"] = "Here is the solution to your coding problem"
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state 

#solving simplle question function
def solve_simple_question(state:State):
    user_message = state.get("user_message")

    
    
    #openai api call ( cooding question gpt-4o-mini)
    SYSTEM_PROMPT = """
You are an AI assistant. Your job is to chat with user.
    """

    #openai api call 
    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=CoodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": user_message }
        
            ],
        
    )
    # state["ai_message"] = "Please ask some coding related question"
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state 


# Create a state graph
graph_builder = StateGraph(State)

# register nodes
graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_question", solve_coding_question)
graph_builder.add_node("solve_simple_question", solve_simple_question)
graph_builder.add_node("route_edge", route_edge)

# register start node
# go to detect_query after start
graph_builder.add_edge(START, "detect_query")
graph_builder.add_conditional_edges("detect_query", route_edge )

graph_builder.add_edge("solve_coding_question", END)
graph_builder.add_edge("solve_simple_question",END)

graph = graph_builder.compile()


# use the graph
def call_graph():
    state = {
        "user_message": "hello ji ",
        "ai_message": "",
        "is_coding_question": False
    }

    result = graph.invoke(state)

    print("final result",result)

call_graph()