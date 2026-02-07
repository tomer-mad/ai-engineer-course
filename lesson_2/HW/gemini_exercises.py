import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# It's recommended to set up your API key as an environment variable for security.
# On your terminal, you can do this by running:
# export GOOGLE_API_KEY="YOUR_API_KEY"
# If you're using a platform like Google Colab, manage your keys securely there.
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini API with your key.
# This step is crucial for authenticating your requests to the API.
genai.configure(api_key=API_KEY)

# --- Exercise 1: Simple Text Completion ---
# Goal: Create a Python script that sends a prompt to Gemini and prints the generated response.
# Focus: API setup, handling responses.
def simple_text_completion():
    """
    Sends a simple text prompt to the Gemini API and prints the response.
    This function demonstrates the most basic interaction with the API.
    """
    print("--- Running Exercise 1: Simple Text Completion ---")
    
    # Initialize the generative model. 'gemini-pro' is a versatile model for text-based tasks.
    model = genai.GenerativeModel('gemini-pro')
    
    # The prompt is the question or instruction you want to send to the model.
    prompt = "Explain black holes like I’m 10 years old."
    print(f"Prompt: {prompt}")
    
    # The `generate_content` method sends the prompt to the API.
    # It returns a response object that contains the generated text and other metadata.
    response = model.generate_content(prompt)
    
    # The generated text is accessed through the `text` attribute of the response.
    # It's always a good idea to check if the response has text before printing.
    if response.text:
        print("\nGemini's Response:")
        print(response.text)
    else:
        print("No response was generated.")

# --- Exercise 2: Chat Memory Simulation ---
# Goal: Build a chat loop that keeps conversation history in a list and sends it as context to Gemini.
# Focus: Maintain session memory, manage role-based conversation structure (user, model).
def chat_memory_simulation():
    """
    Simulates a chat with memory, where the conversation history is maintained.
    This allows for follow-up questions and a more natural conversational flow.
    """
    print("\n--- Running Exercise 2: Chat Memory Simulation ---")
    print("Start chatting with Gemini! Type 'quit' to exit.")

    # Initialize the model.
    model = genai.GenerativeModel('gemini-pro')
    
    # Start a chat session. This creates a `ChatSession` object that automatically
    # stores the history of the conversation.
    chat = model.start_chat(history=[])

    while True:
        # Get input from the user.
        user_input = input("You: ")
        
        # Provide a way for the user to exit the chat loop.
        if user_input.lower() == 'quit':
            print("Chat ended. Goodbye!")
            break
            
        # Send the user's message to the chat. The `send_message` method
        # automatically adds the user's message and the model's response to the history.
        response = chat.send_message(user_input)
        
        # Print the model's response.
        print(f"Gemini: {response.text}")

# --- Exercise 3: Generate Marketing Content ---
# Goal: Create a script that asks the user for a product name and audience, and Gemini generates a short product description, 3 ad slogans, and 1 call-to-action.
# Focus: Structured multi-response generation, prompt templating.
def generate_marketing_content():
    """
    Generates marketing content based on user input for a product and audience.
    This demonstrates how to structure prompts to get specific, multi-part outputs.
    """
    print("\n--- Running Exercise 3: Generate Marketing Content ---")
    
    product_name = input("Enter the product name: ")
    audience = input("Enter the target audience: ")
    
    # A template for the prompt makes it easy to insert user-provided details.
    # This is a key technique for creating dynamic and reusable prompts.
    prompt = f"""
    Generate marketing content for a product with the following details:
    Product Name: {product_name}
    Target Audience: {audience}

    Please provide the following:
    1. A short, engaging product description (2-3 sentences).
    2. Three distinct ad slogans.
    3. One compelling call-to-action.
    """
    
    print("\nGenerating content...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    if response.text:
        print("\n--- Generated Marketing Content ---")
        print(response.text)
    else:
        print("Could not generate marketing content.")

# --- Exercise 4: Summarize a Web Page ---
# Goal: Fetch the content of a given URL using requests, clean the text, and ask Gemini to summarize it.
# Focus: Web scraping, prompting with external data.
def summarize_web_page():
    """
    Fetches text from a URL, cleans it, and uses Gemini to summarize the content.
    This shows how to integrate external data (from the web) into a prompt.
    """
    print("\n--- Running Exercise 4: Summarize a Web Page ---")
    url = input("Enter the URL of the web page to summarize: ")

    try:
        # Use the requests library to get the HTML content of the page.
        response = requests.get(url)
        # Raise an exception if the request was not successful (e.g., 404 Not Found).
        response.raise_for_status()
        
        # Use BeautifulSoup to parse the HTML and extract only the text.
        # This helps to remove HTML tags and other non-textual elements.
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get all the text from the page.
        text = soup.get_text(separator='\n', strip=True)
        
        # A simple way to clean up the text: limit its length to avoid exceeding API limits.
        # For very large pages, more sophisticated chunking would be needed.
        if len(text) > 10000:
            text = text[:10000]

        print("\nSummarizing content...")
        
        model = genai.GenerativeModel('gemini-pro')
        
        # The prompt clearly instructs the model what to do with the provided text.
        prompt = f"Please summarize the following text from a web page:\n\n{text}"
        
        summary_response = model.generate_content(prompt)
        
        if summary_response.text:
            print("\n--- Summary ---")
            print(summary_response.text)
        else:
            print("Failed to generate a summary.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Exercise 5: AI-Powered Code Reviewer ---
# Goal: Read a Python file and send its contents to Gemini asking: 'Review this code for readability and efficiency.'
# Focus: Handling large text inputs, structured feedback generation.
def ai_code_reviewer():
    """
    Reads a Python file and asks Gemini to review it for readability and efficiency.
    This is a practical example of using an LLM for a development task.
    """
    print("\n--- Running Exercise 5: AI-Powered Code Reviewer ---")
    
    # For this example, we'll just review the current file itself.
    # You could modify this to ask the user for a file path.
    file_path = __file__ 
    
    try:
        with open(file_path, 'r') as f:
            code_content = f.read()
            
        prompt = f"""
        Please review the following Python code for readability and efficiency.
        Provide specific suggestions for improvement if you find any.

        ```python
        {code_content}
        ```
        """
        
        print(f"Asking Gemini to review '{file_path}'...")
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response.text:
            print("\n--- Code Review ---")
            print(response.text)
        else:
            print("Could not get a code review.")
            
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Exercise 6: Multi-Modal Caption Generator (Text + Image) ---
# Goal: Upload an image and ask Gemini to generate a descriptive caption and 3 hashtags.
# Focus: Image + text input, using Gemini’s multi-modal capabilities.
def multi_modal_caption_generator():
    """
    Uploads an image file and asks Gemini to generate a caption and hashtags.
    This demonstrates using the genai File API for multi-modal input.
    """
    print("\n--- Running Exercise 6: Multi-Modal Caption Generator ---")
    
    image_path = "cat.jpg"
    uploaded_file = None  # To hold the file object for cleanup
    
    try:
        print(f"Uploading file: {image_path}...")
        # Upload the file to the Gemini API using the genai package's File API.
        # This is the recommended approach for handling files.
        uploaded_file = genai.upload_file(path=image_path, display_name="Cat Image")
        print(f"Completed upload: {uploaded_file.uri}")

        # Initialize the multi-modal model.
        model = genai.GenerativeModel('gemini-pro-vision')
        
        prompt = "Generate a descriptive caption and 3 relevant hashtags for this image."
        
        # Pass the prompt and the uploaded file object to the model.
        # The SDK handles the details of referencing the uploaded file.
        response = model.generate_content([prompt, uploaded_file])
        
        if response.text:
            print("\n--- Generated Content ---")
            print(response.text)
        else:
            print("Could not generate content for the image.")
            
    except FileNotFoundError:
        print(f"Error: The image file '{image_path}' was not found. Please make sure it's in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Important: Clean up by deleting the uploaded file.
        # Files uploaded to the API persist until they are deleted.
        if uploaded_file:
            print(f"Deleting uploaded file: {uploaded_file.name}")
            genai.delete_file(uploaded_file.name)

# --- Exercise 7: CSV Data Insights ---
# Goal: Load a CSV file and ask Gemini to summarize key insights or trends.
# Focus: Data preprocessing, feeding Gemini structured text.
def csv_data_insights():
    """
    Reads a CSV file, converts it to a string, and asks Gemini to provide insights.
    This demonstrates how to use LLMs for basic data analysis.
    """
    print("\n--- Running Exercise 7: CSV Data Insights ---")
    
    csv_path = "sales.csv"
    
    try:
        # Use the pandas library to read the CSV file. This is the standard tool for data manipulation in Python.
        df = pd.read_csv(csv_path)
        
        # Convert the DataFrame to a string format that's easy for the LLM to understand.
        data_string = df.to_string()
        
        prompt = f"""
        Analyze the following sales data and provide key insights or trends.
        What can you tell me about the product sales?

        Data:
        {data_string}
        """
        
        print("Analyzing CSV data...")
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        if response.text:
            print("\n--- Data Insights ---")
            print(response.text)
        else:
            print("Could not generate insights from the data.")
            
    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Exercise 8: RAG-style Document Q&A ---
# Goal: Read a text document, and answer user questions using only the text context.
# Focus: Context injection, Retrieval-Augmented Generation (RAG) concept.
def rag_document_qa():
    """
    Answers questions based on the content of a text file.
    This simulates a simple Retrieval-Augmented Generation (RAG) system.
    """
    print("\n--- Running Exercise 8: RAG-style Document Q&A ---")
    
    doc_path = "report.txt"
    
    try:
        with open(doc_path, 'r') as f:
            document_text = f.read()
            
        print("Document loaded. Ask a question about the document (type 'quit' to exit).")
        
        while True:
            question = input("Your Question: ")
            if question.lower() == 'quit':
                break
            
            # The prompt is structured to force the model to answer based *only* on the provided context.
            # This is the core idea of RAG: retrieve relevant information and provide it to the model.
            prompt = f"""
            Based *only* on the following document, please answer the question.
            If the answer is not in the document, say 'The answer is not in the document.'

            Document:
            ---
            {document_text}
            ---

            Question: {question}
            """
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            if response.text:
                print(f"Answer: {response.text}")
            else:
                print("I could not generate an answer.")

    except FileNotFoundError:
        print(f"Error: The document '{doc_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Exercise 9: Emotion Analysis of Reviews ---
# Goal: Take a list of product reviews and ask Gemini to return the dominant emotion and a sentiment score (1-5) for each.
# Focus: Structured output parsing (JSON), text classification with LLMs.
def emotion_analysis_of_reviews():
    """
    Performs emotion and sentiment analysis on a list of reviews, requesting JSON output.
    This shows how to get structured data from the model, which is crucial for many applications.
    """
    print("\n--- Running Exercise 9: Emotion Analysis of Reviews ---")
    
    reviews = [
        "The battery life is amazing! Lasts for days.",
        "The screen is a bit dim, and it's hard to see in the sun.",
        "I am absolutely furious with the customer service.",
        "It's an okay product, nothing special but it gets the job done."
    ]
    
    # Instructing the model to return a JSON object makes the output predictable and easy to parse.
    prompt = f"""
    Analyze each of the following product reviews.
    For each review, provide the dominant emotion and a sentiment score from 1 (very negative) to 5 (very positive).
    Return the output as a JSON array where each object has 'review', 'emotion', and 'score' keys.

    Reviews:
    {json.dumps(reviews)}
    """
    
    print("Analyzing reviews...")
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    try:
        # The response text is cleaned up to extract the JSON part.
        # LLMs can sometimes add extra text like "Here is the JSON:"
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        
        # The `json.loads` function parses the JSON string into a Python list of dictionaries.
        results = json.loads(json_text)
        
        print("\n--- Analysis Results ---")
        for result in results:
            print(f"Review: '{result['review']}' -> Emotion: {result['emotion']}, Score: {result['score']}")
            
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON response: {e}")
        print("Raw response was:\n", response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Exercise 10: Create a Gemini-Powered Chatbot (Flask API) ---
# Goal: Build a Flask app exposing a /chat endpoint.
# Focus: Backend API integration, reusable AI microservice pattern.
def flask_chatbot_instructions():
    """
    Provides instructions and code for creating a simple Flask-based chatbot.
    Since running a web server from this script is complex, this function will
    print the code and instructions for the user to run it separately.
    """
    print("\n--- Exercise 10: Create a Gemini-Powered Chatbot (Flask API) ---")
    print("This exercise involves running a web server, which should be done in a separate file.")
    print("Here is the code and the steps to run it:\n")
    
    # Code for the Flask application
    flask_code = """
# 1. Save this code as 'app.py'
# 2. Install Flask: pip install Flask
# 3. Run the app: python app.py
# 4. Open a new terminal and send a request:
#    curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello"}' http://127.0.0.1:5000/chat

from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# --- Configuration ---
# Make sure your GOOGLE_API_KEY is set as an environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Chat Endpoint ---
@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the JSON payload
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Initialize the model and send the message
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)
        
        # Return the model's response
        return jsonify({"reply": response.text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Main Execution ---
if __name__ == '__main__':
    # Runs the Flask app on a local development server.
    # Host '0.0.0.0' makes it accessible from your network.
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
    print("="*60)
    print(flask_code)
    print("="*60)


# --- Main execution block ---
def main():
    """
    Main function to display a menu and run the selected exercise.
    This makes it easy to test each function individually.
    """
    exercises = {
        "1": simple_text_completion,
        "2": chat_memory_simulation,
        "3": generate_marketing_content,
        "4": summarize_web_page,
        "5": ai_code_reviewer,
        "6": multi_modal_caption_generator,
        "7": csv_data_insights,
        "8": rag_document_qa,
        "9": emotion_analysis_of_reviews,
        "10": flask_chatbot_instructions,
    }

    while True:
        print("\n--- Python + Gemini API Exercises ---")
        print("1. Simple Text Completion")
        print("2. Chat Memory Simulation")
        print("3. Generate Marketing Content")
        print("4. Summarize a Web Page")
        print("5. AI-Powered Code Reviewer")
        print("6. Multi-Modal Caption Generator")
        print("7. CSV Data Insights")
        print("8. RAG-style Document Q&A")
        print("9. Emotion Analysis of Reviews")
        print("10. Flask Chatbot Instructions")
        print("Type 'exit' to quit.")
        
        choice = input("Choose an exercise to run (1-10): ")

        if choice.lower() == 'exit':
            break
        
        exercise_func = exercises.get(choice)
        
        if exercise_func:
            exercise_func()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
