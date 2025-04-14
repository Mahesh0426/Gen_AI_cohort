from dotenv import load_dotenv
from openai import OpenAI

# Loads your API key from the .env file
load_dotenv()

 # Creates an OpenAI client to talk to the API
client = OpenAI()

text = " Eiffel tower is in Paris and is a famous landmarks, it is 324 meters tall"

# Create the vector embedding using OpenAI
response = client.embeddings.create(
    input = text, 
    model = "text-embedding-3-small"
)

print("vector embedding:",response.data[0].embedding)