from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os 
load_dotenv()

client =  OpenAI()

def run_command(command):
    result = os.system(command=command)
    return result

# print(run_command("ls"))

#function to call api
def get_weather(city:str):
    print(f"getting weather for {city}")

    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "something wrong"

def add(x, y):
    print("🔨 Tool Called: add", x, y)
    return x + y

avaiable_tools= {
    "get_weather": {
        'fn':get_weather,
        'description': "Takes a city name as an input and returns the current weather for the city",
    },
    "run_command":{
        "fn":run_command,
        "description": "Take a command as an input to execute command on the system and returns output"
    }
}

# system prompt
system_prompt = """ 
You are an helpful AI Asssistant who is specialized in resolving user query.
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step exececution, based on the planning,
 select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool
 wait for the obversation and based on observation from the tool call resolve the user query.

 Rules:
 - Follow the Output JSON format
 - Always perform one step at a time and wait for the next input
 - Carefully analyse the user query 

 Output JSON format:
 {{
 "step":"string",
 "content": "string"'
 "function":"The  name of function if the step is action",
 "input": "The input paramater for the function",
 }}

 Available Tools:
- get_weather: Takes a city name as an input and returns the current weather for the city
- run_command: Take a command as an input to execute command on the system and returns output

 Example:
 User Query: What is the weather of new york ?
 outputL{{"step:"plan", "content":"The user is interested in weather data of new york"}}
 outputL{{"step:"plan", "content":"From the available tools I should call get_weather"}}
 outputL{{"step:"action", "function":"get_weather", "input":"new york"}}
 outputL{{"step:"observe", "output":12 Degree Cel"}}
 outputL{{"step:"output", "contetn": Weather for new york eems to be  12 Degree Cel"}}

"""

messages = [
{"role":"system", "content": system_prompt}
]



while True:
    user_query = input('> ')
    messages.append({"role":"user","content":user_query})


    while True:
        response = client.chat.completions.create(
            model = "gpt-4o",
            response_format={"type":"json_object"},
            messages = messages 
        )
        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        if parsed_output.get("step")== "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name, False) != False:
                output = avaiable_tools[tool_name].get("fn")(tool_input)
                messages.append({"role":"assistant", "content": json.dumps({"step":"observe", "output": output})})
                continue

        if parsed_output.get("step")== "output":
            print(f"🤖: {parsed_output.get("content")}")
            break
    
    
           
        





