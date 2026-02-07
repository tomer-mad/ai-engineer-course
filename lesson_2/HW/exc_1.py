from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

"""
  Sends a simple text prompt to the Gemini API and prints the response.
  This function demonstrates the most basic interaction with the API.
  """
print("--- Running Exercise 1: Simple Text Completion ---")

# The prompt is the question or instruction you want to send to the model.
prompt = "Explain black holes like I'm 10 years old."
print(f"Prompt: {prompt}")

# The `generate_content` method sends the prompt to the API.
# It returns a response object that contains the generated text and other metadata.
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
)

# The generated text is accessed through the `text` attribute of the response.
if response.text:
    print("\nGemini's Response:")
    print(response.text)
else:
    print("No response was generated.")

