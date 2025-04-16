from dotenv import load_dotenv
from openai import OpenAI
import json


load_dotenv()

client =  OpenAI()

system_prompt =  """ You are an AI assistance who is expert in breaking down complex problems  and then resolve the user query.

For a given  user input, analyse the input and break down the problem  step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again  think for several times and then return an output with explanation and then finally you validate the output as well before giving final results.

Follow the steps in sequence that is "analyse", "think", "outpout", "validate" and  finally "result":.

Rules:
1. Folow the strict JSON output as per the output schema.
2. Always perform one step at a time  and wait for next input.
3. Carefully analyse the user query

Output Format:
{{step: "string", content: "string"}}

Example:
Input:  what is 2 + 2 ?
Output: {{step:"analyse", content: " Alright!,  the user is interested in maths query and he is asking a basic arithmetic operation."}}
output:{{step: "think", content: "To perform addition, I must  go from left to right  and add all the operands."}}
output:{{step: "output", content: "4"}}
output:{{step: "validate", content: "seems like 4 is correct ans for 2 + 2."}}
outputL{{step: "result", content:"2 + 2 = 4 and that is calculatd by addiing all numbers.}}

"""

result = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type":"json_object"},
    messages = [
        {"role":"system", "content":system_prompt},
        {"role":"user" , "content": "what is 3 +4 * 5 ? "},
        {"role":"assistant", "content": json.dumps({"step": "analyse", "content": "The user is asking a mathematics question involving multiple arithmetic operations: addition and multiplication."}) },
        {"role":"assistant", "content": json.dumps({"step": "think", "content": "To solve this, I should remember the order of operations, often abbreviated as PEMDAS (Parentheses, Exponents, Multiplication and Division (from left to right), Addition and Subtraction (from left to right)). Here, multiplication should be performed before addition."}) },
        {"role":"assistant", "content": json.dumps({"step": "think", "content": "According to the order of operations, I first need to perform the multiplication: 4 * 5."}) },
        {"role":"assistant", "content": json.dumps({"step": "think", "content": "Once the multiplication is done, I will add the result to 3 to get the final answer."}) },


    ],
)

print(result.choices[0].message.content)

