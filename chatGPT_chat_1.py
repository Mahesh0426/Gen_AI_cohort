from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client =  OpenAI()

system_prompt =  """You are an AI assistance who is specialized in maths. You should not answer any query that is not related to maths.

For a given help user to solve that along with experience.

Example: 
Input: 2 + 2 
Output: 2 + 2 is 4 which is calculated by adding 2 and 2.

Input: 3 * 10 
Output: 3 * 10 is 30 which is calculated by multiplying 3 and 10.Funfact you can even multiply 10 * 3 which give same result.

Input: why is the sky blue ?
Output: Bruh! are you  serious ? I am a math expert.

"""

result = client.chat.completions.create(
    model="gpt-4",
    messages = [
        {"role":"system", "content":system_prompt},
        {"role":"user" , 
        # "content": "what is mobile phone  ? "},
        "content": "what is 3 * 5 ? "},

    ],
)

print(result.choices[0].message.content)

