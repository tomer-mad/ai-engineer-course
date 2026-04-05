import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
ai_model = "gemini-2.0-flash"
response = client.models.generate_content(
    model=ai_model,
    contents="what is the capital of france",
)

print(response.text)