# chain of throught prompting
from dotenv import load_dotenv
from openai import OpenAI
import json
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)


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


messages = [
     {"role":"system", "content":system_prompt},
]

query = input ("> ")
messages.append({"role":"user", "content": query})

while True:
  
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"json_object"},
        messages = messages,
    )

    parse_response = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant", "content": json.dumps(parse_response)})

    if parse_response.get("step") != "output":
       
        print(f"{Fore.CYAN}🧠 Step: {parse_response.get('step').upper()}")
        print(f"{Fore.YELLOW}{parse_response.get('content')}")
        continue 

    print("\n")
    print(f"{Fore.GREEN}🤖 FINAL OUTPUT")
    print(f"{Fore.WHITE}{Style.BRIGHT}{parse_response.get('content')}")
    break

   

    # if parse_response.get("step") != "output":
    #     print(f"🧠:{parse_response.get("content")}")
    #     continue
    # print(f"🤖: {parse_response.get("content")}")
    # break


