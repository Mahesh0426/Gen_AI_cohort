from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")


# Pass it to the client
client = genai.Client(api_key=api_key)




response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='what is 2 * 6'
)
print(response.text)