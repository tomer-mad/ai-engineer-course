"""
=============================================================================
Python + Gemini API: 10 Practical Exercises - Solutions
=============================================================================

This file contains solutions to all 10 Gemini API exercises.
Each exercise is implemented as a function with detailed comments.

SETUP REQUIRED:
1. Create a .env file with your API key: GOOGLE_API_KEY=your_key_here
2. Install required packages: pip install google-genai python-dotenv requests beautifulsoup4 flask

HOW TO RUN:
Run this script and select which exercise you want to execute from the menu.
"""

# =============================================================================
# IMPORTS - Libraries we need for all exercises
# =============================================================================

# google.genai - The official Google Generative AI library for Python
from google import genai

# os - For accessing environment variables (like our API key)
import os

# dotenv - Loads environment variables from a .env file
from dotenv import load_dotenv

# json - For parsing JSON responses (used in Exercise 9)
import json

# csv - For reading CSV files (used in Exercise 7)
import csv

# requests - For making HTTP requests to fetch web pages (Exercise 4)
import requests

# BeautifulSoup - For parsing HTML content (Exercise 4)
from bs4 import BeautifulSoup

# base64 - For encoding images (Exercise 6)
import base64

# pathlib - For handling file paths easily
from pathlib import Path

# =============================================================================
# INITIAL SETUP - Load API key and create client
# =============================================================================

# Load environment variables from .env file
# This is where we store our API key securely (never commit .env to git!)
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

# Create the Gemini client - this is our connection to the API
# We'll use this client in all exercises to communicate with Gemini
client = genai.Client(api_key=API_KEY)

# "gemini-2.0-flash" is fast and good for most tasks
MODEL_NAME = "gemini-2.0-flash"


# =============================================================================
# EXERCISE 1: Simple Text Completion
# =============================================================================
# Goal: Create a Python script that sends a prompt to Gemini and prints
#       the generated response.
# Example Task: Prompt → 'Explain black holes like I'm 10 years old.'
# Focus:
#   - API setup
#   - Handling responses
# =============================================================================

def exercise_1_simple_text_completion():
    """
    Sends a simple text prompt to the Gemini API and prints the response.
    This is the most basic way to interact with the API.
    """
    print("\n" + "="*60)
    print("EXERCISE 1: Simple Text Completion")
    print("="*60)

    # The prompt is what we want to ask or tell the AI
    # You can change this to any question or instruction
    prompt = "Explain black holes like I'm 10 years old."

    print(f"\nYour Prompt: {prompt}")
    print("\nSending to Gemini...\n")

    # KEY CONCEPT: generate_content() is the main method to get AI responses
    # - model: which AI model to use
    # - contents: the prompt/question we want answered
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    # The response object contains the generated text in the 'text' attribute
    # Always check if text exists before using it
    if response.text:
        print("Gemini's Response:")
        print("-" * 40)
        print(response.text)
    else:
        print("No response was generated.")


# =============================================================================
# EXERCISE 2: Chat Memory Simulation
# =============================================================================
# Goal: Build a chat loop that keeps conversation history in a list and
#       sends it as context to Gemini.
# Focus:
#   - Maintain session memory
#   - Manage role-based conversation structure (user, model)
# =============================================================================

def exercise_2_chat_memory():
    """
    Creates an interactive chat that remembers the conversation history.
    Each message is stored and sent as context for the next response.
    """
    print("\n" + "="*60)
    print("EXERCISE 2: Chat Memory Simulation")
    print("="*60)
    print("\nStarting chat with memory. Type 'quit' to exit.\n")

    # KEY CONCEPT: conversation_history stores all messages
    # This list will grow as the conversation continues
    # Each message has a 'role' (user or model) and 'parts' (the text)
    conversation_history = []

    while True:
        # Get user input
        user_input = input("You: ").strip()

        # Check if user wants to quit
        if user_input.lower() == 'quit':
            print("\nEnding chat. Goodbye!")
            break

        # Skip empty inputs
        if not user_input:
            continue

        # KEY CONCEPT: Add the user's message to history
        # 'role': 'user' means this message is from the human
        # 'parts': contains the actual text content
        conversation_history.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })

        # Send the ENTIRE conversation history to Gemini
        # This is how the AI "remembers" what was said before
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation_history,
        )

        # Get the AI's response text
        ai_response = response.text if response.text else "I couldn't generate a response."

        # KEY CONCEPT: Add the AI's response to history too
        # 'role': 'model' means this message is from the AI
        conversation_history.append({
            "role": "model",
            "parts": [{"text": ai_response}]
        })

        # Display the response
        print(f"\nGemini: {ai_response}\n")


# =============================================================================
# EXERCISE 3: Generate Marketing Content
# =============================================================================
# Goal: Create a script that asks the user for a product name and audience,
#       and Gemini generates:
#       - A short product description
#       - 3 ad slogans
#       - 1 call-to-action
# Focus:
#   - Structured multi-response generation
#   - Prompt templating
# =============================================================================

def exercise_3_marketing_content():
    """
    Generates marketing content (description, slogans, CTA) for a product.
    Demonstrates how to use prompt templates for structured output.
    """
    print("\n" + "="*60)
    print("EXERCISE 3: Generate Marketing Content")
    print("="*60)

    # Get product information from user
    product_name = input("\nEnter the product name: ").strip()
    target_audience = input("Enter the target audience (e.g., 'young professionals', 'parents'): ").strip()

    # KEY CONCEPT: Prompt Template
    # A well-structured prompt helps get well-structured responses
    # We're being very specific about what we want the AI to generate
    prompt_template = f"""
You are a marketing expert. Create marketing content for the following product:

Product Name: {product_name}
Target Audience: {target_audience}

Please generate:
1. A short product description (2-3 sentences)
2. Three catchy advertising slogans
3. One compelling call-to-action

Format your response clearly with headers for each section.
"""

    print("\nGenerating marketing content...")

    # Send the templated prompt to Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt_template,
    )

    if response.text:
        print("\n" + "-"*40)
        print("GENERATED MARKETING CONTENT:")
        print("-"*40)
        print(response.text)
    else:
        print("Failed to generate content.")


# =============================================================================
# EXERCISE 4: Summarize a Web Page
# =============================================================================
# Goal: Fetch the content of a given URL using requests, clean the text,
#       and ask Gemini to summarize it.
# Focus:
#   - Web scraping
#   - Prompt with external data
# =============================================================================

def exercise_4_summarize_webpage():
    """
    Fetches a webpage, extracts its text content, and asks Gemini to summarize it.
    Demonstrates combining web scraping with AI summarization.
    """
    print("\n" + "="*60)
    print("EXERCISE 4: Summarize a Web Page")
    print("="*60)

    # Get URL from user (with a default example)
    url = input("\nEnter a URL to summarize (or press Enter for example): ").strip()

    # Default URL for testing
    if not url:
        url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
        print(f"Using example URL: {url}")

    print(f"\nFetching content from: {url}")

    try:
        # KEY CONCEPT: Use requests library to fetch web page content
        # headers: Some websites block requests without a user-agent
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error for bad status codes

        # KEY CONCEPT: Use BeautifulSoup to parse HTML
        # This helps us extract just the text, not the HTML tags
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements (they contain code, not content)
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()

        # Get the text content
        text_content = soup.get_text(separator=' ', strip=True)

        # Limit text length to avoid overwhelming the API
        # Most pages have way more text than we need
        max_chars = 5000
        if len(text_content) > max_chars:
            text_content = text_content[:max_chars] + "..."
            print(f"Note: Text truncated to {max_chars} characters")

        print("Content fetched! Asking Gemini to summarize...\n")

        # KEY CONCEPT: Combine external data with a prompt
        # We're giving the AI the webpage content as context
        summary_prompt = f"""
Please summarize the following webpage content in 3-5 bullet points.
Focus on the main ideas and key information.

WEBPAGE CONTENT:
{text_content}

SUMMARY:
"""

        # Send to Gemini for summarization
        ai_response = client.models.generate_content(
            model=MODEL_NAME,
            contents=summary_prompt,
        )

        if ai_response.text:
            print("-"*40)
            print("SUMMARY:")
            print("-"*40)
            print(ai_response.text)
        else:
            print("Failed to generate summary.")

    # KEY CONCEPT: Specific exception handling
    # Using specific exceptions helps give better error messages to users
    except requests.exceptions.Timeout:
        print("Error: The request timed out. The website took too long to respond.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the website. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: The website returned an error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# =============================================================================
# EXERCISE 5: AI-Powered Code Reviewer
# =============================================================================
# Goal: Read a Python file and send its contents to Gemini asking:
#       'Review this code for readability and efficiency.'
# Focus:
#   - Handling large text inputs
#   - Structured feedback generation
# =============================================================================

def exercise_5_code_reviewer():
    """
    Reads a Python file and asks Gemini to review it for readability and efficiency.
    Demonstrates how to use AI for code review assistance.
    """
    print("\n" + "="*60)
    print("EXERCISE 5: AI-Powered Code Reviewer")
    print("="*60)

    # Get the file path from user
    file_path = input("\nEnter the path to a Python file to review (or press Enter for this file): ").strip()

    # Default to reviewing this file itself!
    if not file_path:
        file_path = __file__  # __file__ is the path to the current script
        print(f"Reviewing: {file_path}")

    try:
        # KEY CONCEPT: Read file contents using Python's open()
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()

        # Limit code length to avoid API limits
        max_chars = 10000
        if len(code_content) > max_chars:
            code_content = code_content[:max_chars]
            print(f"Note: Code truncated to {max_chars} characters for review")

        print("\nCode loaded! Sending to Gemini for review...\n")

        # KEY CONCEPT: Structured review prompt
        # We ask for specific categories of feedback
        review_prompt = f"""
You are an experienced Python code reviewer.
Please review the following code and provide feedback on:

1. **Readability**: Is the code easy to understand? Are variable names clear?
2. **Efficiency**: Are there any performance improvements possible?
3. **Best Practices**: Does the code follow Python conventions (PEP 8)?
4. **Suggestions**: What specific improvements would you recommend?

Keep your review concise and beginner-friendly.

CODE TO REVIEW:
```python
{code_content}
```

REVIEW:
"""

        # Send to Gemini
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=review_prompt,
        )

        if response.text:
            print("-"*40)
            print("CODE REVIEW:")
            print("-"*40)
            print(response.text)
        else:
            print("Failed to generate review.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# =============================================================================
# EXERCISE 6: Multi-Modal Caption Generator (Text + Image)
# =============================================================================
# Goal: Upload an image (e.g., cat.jpg) and ask Gemini to generate:
#       - A descriptive caption
#       - 3 hashtags
# Focus:
#   - Image + text input
#   - Using Gemini's multi-modal capabilities
# =============================================================================

def exercise_6_image_caption():
    """
    Loads an image and asks Gemini to generate a caption and hashtags.
    Demonstrates multi-modal (image + text) capabilities.
    """
    print("\n" + "="*60)
    print("EXERCISE 6: Multi-Modal Caption Generator")
    print("="*60)

    # Get image path from user
    image_path = input("\nEnter the path to an image file (jpg, png): ").strip()

    if not image_path:
        print("No image path provided. Please provide an image file.")
        print("Example: /path/to/your/image.jpg")
        return

    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return

    try:
        print(f"\nLoading image: {image_path}")

        # KEY CONCEPT: Read and encode the image as base64
        # Base64 converts binary image data to text that can be sent to the API
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Determine the image type (mime type)
        # This tells the API what format the image is in
        image_extension = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(image_extension, 'image/jpeg')

        print("Image loaded! Generating caption...\n")

        # KEY CONCEPT: Multi-modal prompt - combining image and text
        # We send both the image and a text prompt together
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                # The text part - our instruction
                {
                    "role": "user",
                    "parts": [
                        {"text": """Look at this image and generate:
1. A descriptive caption (1-2 sentences describing what's in the image)
2. Three relevant hashtags for social media

Format:
Caption: [your caption here]
Hashtags: #tag1 #tag2 #tag3"""},
                        # The image part - the actual image data
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64.b64encode(image_data).decode('utf-8')
                            }
                        }
                    ]
                }
            ],
        )

        if response.text:
            print("-"*40)
            print("GENERATED CONTENT:")
            print("-"*40)
            print(response.text)
        else:
            print("Failed to generate caption.")

    except Exception as e:
        print(f"An error occurred: {e}")


# =============================================================================
# EXERCISE 7: CSV Data Insights
# =============================================================================
# Goal: Load a CSV file (e.g., sales.csv) and ask Gemini to summarize
#       key insights or trends.
# Focus:
#   - Data preprocessing
#   - Feeding Gemini structured text
# =============================================================================

def exercise_7_csv_insights():
    """
    Loads a CSV file and asks Gemini to analyze and provide insights.
    Demonstrates how to feed structured data to an LLM.
    """
    print("\n" + "="*60)
    print("EXERCISE 7: CSV Data Insights")
    print("="*60)

    # Get CSV file path
    csv_path = input("\nEnter the path to a CSV file (or press Enter for sales.csv): ").strip()

    # Default to the included sales.csv
    if not csv_path:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "sales.csv")
        print(f"Using: {csv_path}")

    try:
        # KEY CONCEPT: Read CSV file and convert to text
        # We'll format the data nicely so the AI can understand it
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Read CSV with the csv library
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            print("CSV file is empty.")
            return

        # Format CSV data as a readable table
        # This makes it easier for the AI to understand the structure
        csv_text = "\n".join([", ".join(row) for row in rows])

        print(f"\nLoaded {len(rows)-1} data rows (plus header)")
        print("\nCSV Content Preview:")
        print("-"*40)
        # Show first few rows
        for row in rows[:6]:
            print(", ".join(row))
        if len(rows) > 6:
            print("...")
        print("-"*40)

        print("\nAsking Gemini for insights...\n")

        # KEY CONCEPT: Ask AI to analyze structured data
        analysis_prompt = f"""
Analyze the following CSV data and provide:

1. **Summary**: What does this data represent?
2. **Key Insights**: What patterns or trends do you notice?
3. **Statistics**: Any notable numbers (totals, averages, etc.)?
4. **Recommendations**: Based on this data, what actions might be useful?

CSV DATA:
{csv_text}

ANALYSIS:
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=analysis_prompt,
        )

        if response.text:
            print("-"*40)
            print("DATA INSIGHTS:")
            print("-"*40)
            print(response.text)
        else:
            print("Failed to generate insights.")

    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# =============================================================================
# EXERCISE 8: RAG-style Document Q&A
# =============================================================================
# Goal: Read a text document (report.txt), chunk it, and send user questions
#       to Gemini to answer using only the text context.
# Focus:
#   - Context injection
#   - Retrieval-Augmented Generation concept
# =============================================================================

def exercise_8_document_qa():
    """
    Implements a simple RAG (Retrieval-Augmented Generation) system.
    Loads a document and answers questions based ONLY on that document.
    """
    print("\n" + "="*60)
    print("EXERCISE 8: RAG-style Document Q&A")
    print("="*60)

    # Get document path
    doc_path = input("\nEnter the path to a text document (or press Enter for report.txt): ").strip()

    # Default to the included report.txt
    if not doc_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        doc_path = os.path.join(script_dir, "report.txt")
        print(f"Using: {doc_path}")

    try:
        # Read the document content
        with open(doc_path, 'r', encoding='utf-8') as f:
            document_content = f.read()

        print(f"\nDocument loaded! ({len(document_content)} characters)")
        print("\n" + "-"*40)
        print("DOCUMENT PREVIEW:")
        print("-"*40)
        # Show first 500 characters
        preview = document_content[:500]
        print(preview + ("..." if len(document_content) > 500 else ""))
        print("-"*40)

        print("\nYou can now ask questions about this document.")
        print("Type 'quit' to exit.\n")

        while True:
            question = input("Your Question: ").strip()

            if question.lower() == 'quit':
                print("Exiting Q&A session.")
                break

            if not question:
                continue

            # KEY CONCEPT: RAG Prompt
            # We provide the document as context and instruct the AI to
            # ONLY use information from the document to answer
            rag_prompt = f"""
You are a helpful assistant that answers questions based ONLY on the provided document.
If the answer is not in the document, say "I cannot find this information in the document."

DOCUMENT:
{document_content}

QUESTION: {question}

ANSWER (based only on the document above):
"""

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=rag_prompt,
            )

            if response.text:
                print(f"\nAnswer: {response.text}\n")
            else:
                print("Failed to generate answer.\n")

    except FileNotFoundError:
        print(f"Error: File '{doc_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# =============================================================================
# EXERCISE 9: Emotion Analysis of Reviews
# =============================================================================
# Goal: Take a list of product reviews and ask Gemini to return the dominant
#       emotion and sentiment score (1-5) for each.
# Focus:
#   - Structured output parsing (JSON)
#   - Text classification with LLMs
# =============================================================================

def exercise_9_emotion_analysis():
    """
    Analyzes product reviews for emotions and sentiment.
    Demonstrates getting structured JSON output from the AI.
    """
    print("\n" + "="*60)
    print("EXERCISE 9: Emotion Analysis of Reviews")
    print("="*60)

    # Sample reviews for demonstration
    # In a real application, these would come from user input or a database
    sample_reviews = [
        "This product is amazing! Best purchase I've ever made. So happy!",
        "Terrible quality. Broke after one day. Very disappointed and angry.",
        "It's okay, nothing special. Does what it's supposed to do.",
        "I love this! Exceeded all my expectations. Will buy again!",
        "Waste of money. Don't buy this. I regret my purchase."
    ]

    print("\nSample Reviews to Analyze:")
    print("-"*40)
    for i, review in enumerate(sample_reviews, 1):
        print(f"{i}. {review}")
    print("-"*40)

    # Ask if user wants to add custom reviews
    custom = input("\nAdd your own review? (Enter review or press Enter to skip): ").strip()
    if custom:
        sample_reviews.append(custom)

    print("\nAnalyzing emotions and sentiment...\n")

    # KEY CONCEPT: Request JSON output for structured data
    # We explicitly ask for JSON format so we can parse the response
    analysis_prompt = f"""
Analyze the following product reviews and for each one identify:
1. The dominant emotion (e.g., joy, anger, sadness, surprise, fear, neutral)
2. A sentiment score from 1 to 5 (1=very negative, 3=neutral, 5=very positive)

Reviews:
{chr(10).join([f'{i+1}. "{review}"' for i, review in enumerate(sample_reviews)])}

IMPORTANT: Respond ONLY with a valid JSON array in this exact format, no other text:
[
  {{"review_number": 1, "emotion": "emotion_here", "sentiment_score": 5, "brief_explanation": "why"}},
  {{"review_number": 2, "emotion": "emotion_here", "sentiment_score": 1, "brief_explanation": "why"}}
]
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=analysis_prompt,
    )

    if response.text:
        print("-"*40)
        print("ANALYSIS RESULTS:")
        print("-"*40)

        # KEY CONCEPT: Parse JSON response
        # The AI should return JSON that we can parse into Python objects
        try:
            # Clean up the response - remove markdown code blocks if present
            json_text = response.text.strip()
            if json_text.startswith("```"):
                # Remove markdown code block markers
                lines = json_text.split('\n')
                json_text = '\n'.join(lines[1:-1])

            # Parse the JSON
            results = json.loads(json_text)

            # Display results in a nice format
            for result in results:
                review_num = result.get('review_number', '?')
                emotion = result.get('emotion', 'unknown')
                score = result.get('sentiment_score', '?')
                explanation = result.get('brief_explanation', '')

                # Create a visual sentiment bar
                if isinstance(score, int):
                    bar = "★" * score + "☆" * (5 - score)
                else:
                    bar = "?"

                print(f"\nReview #{review_num}")
                print(f"  Emotion: {emotion}")
                print(f"  Sentiment: {bar} ({score}/5)")
                print(f"  Why: {explanation}")

        except json.JSONDecodeError:
            # If JSON parsing fails, just show the raw response
            print("(Could not parse as JSON, showing raw response)")
            print(response.text)
    else:
        print("Failed to analyze reviews.")


# =============================================================================
# EXERCISE 10: Create a Gemini-Powered Chatbot (Flask API)
# =============================================================================
# Goal: Build a Flask app exposing /chat endpoint.
#       Users send messages → Flask routes them to Gemini → returns replies.
# Focus:
#   - Backend API integration
#   - Reusable AI microservice pattern
# =============================================================================

def exercise_10_flask_chatbot():
    """
    Creates a Flask web app with a full chat interface for Gemini.
    This runs a local web server with a beautiful chat UI in the browser.

    NOTE: This exercise requires Flask to be installed.
    Install it with: pip install flask
    """
    print("\n" + "="*60)
    print("EXERCISE 10: Flask Chatbot with Web Interface")
    print("="*60)

    try:
        # Import Flask here so the rest of the file works without it
        from flask import Flask, request, jsonify
    except ImportError:
        print("\nFlask is not installed. Install it with:")
        print("  pip install flask")
        return

    print("""
This exercise creates a web chat interface for Gemini.
Once started, open your browser and go to:

    http://localhost:5000

You'll see a chat interface where you can talk to Gemini directly!

Press Ctrl+C to stop the server.
""")

    input("Press Enter to start the server...")

    # KEY CONCEPT: Create a Flask application
    # Flask is a lightweight web framework for Python
    app = Flask(__name__)

    # Store conversation history (simple in-memory storage)
    # In production, you'd use a database
    conversation_history = []

    # KEY CONCEPT: HTML Template with embedded CSS and JavaScript
    # This creates a complete chat interface in one string
    # In larger projects, you'd use separate template files
    CHAT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Chat</title>
    <style>
        /* KEY CONCEPT: CSS Styling for the chat interface */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .chat-container {
            width: 100%;
            max-width: 800px;
            height: 80vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .chat-header h1 {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }

        .chat-header p {
            opacity: 0.8;
            font-size: 0.9rem;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f5f5f5;
        }

        .message {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }

        .message.user {
            align-items: flex-end;
        }

        .message.bot {
            align-items: flex-start;
        }

        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message.bot .message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .message-label {
            font-size: 0.75rem;
            color: #888;
            margin-bottom: 4px;
            padding: 0 10px;
        }

        .chat-input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
        }

        .chat-input-form {
            display: flex;
            gap: 10px;
        }

        #message-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #eee;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }

        #message-input:focus {
            border-color: #667eea;
        }

        #send-button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        #send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        #send-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .clear-button {
            display: block;
            margin: 10px auto 0;
            padding: 8px 20px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: background 0.3s;
        }

        .clear-button:hover {
            background: #ee5a5a;
        }

        .typing-indicator {
            display: none;
            padding: 12px 18px;
            background: white;
            border-radius: 18px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            width: fit-content;
        }

        .typing-indicator.show {
            display: block;
        }

        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>Gemini Chatbot</h1>
            <p>Powered by Google Gemini AI</p>
        </div>

        <div class="chat-messages" id="chat-messages">
            <!-- Messages will be added here dynamically -->
            <div class="message bot">
                <span class="message-label">Gemini</span>
                <div class="message-content">Hello! I'm Gemini. How can I help you today?</div>
            </div>
            <div class="typing-indicator" id="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>

        <div class="chat-input-container">
            <form class="chat-input-form" id="chat-form">
                <input
                    type="text"
                    id="message-input"
                    placeholder="Type your message here..."
                    autocomplete="off"
                    required
                >
                <button type="submit" id="send-button">Send</button>
            </form>
            <button class="clear-button" id="clear-button">Clear Chat</button>
        </div>
    </div>

    <script>
        // KEY CONCEPT: JavaScript for handling chat interactions
        // This handles sending messages and updating the UI

        const chatMessages = document.getElementById('chat-messages');
        const chatForm = document.getElementById('chat-form');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const clearButton = document.getElementById('clear-button');
        const typingIndicator = document.getElementById('typing-indicator');

        // Function to add a message to the chat
        function addMessage(content, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

            const label = document.createElement('span');
            label.className = 'message-label';
            label.textContent = isUser ? 'You' : 'Gemini';

            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;

            messageDiv.appendChild(label);
            messageDiv.appendChild(contentDiv);

            // Insert before typing indicator
            chatMessages.insertBefore(messageDiv, typingIndicator);

            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Handle form submission
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const message = messageInput.value.trim();
            if (!message) return;

            // Add user message to chat
            addMessage(message, true);
            messageInput.value = '';

            // Disable input while waiting for response
            sendButton.disabled = true;
            messageInput.disabled = true;
            typingIndicator.classList.add('show');

            try {
                // KEY CONCEPT: Fetch API to send message to server
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });

                const data = await response.json();

                if (data.error) {
                    addMessage('Error: ' + data.error, false);
                } else {
                    addMessage(data.response, false);
                }
            } catch (error) {
                addMessage('Error: Could not connect to server.', false);
            }

            // Re-enable input
            sendButton.disabled = false;
            messageInput.disabled = false;
            typingIndicator.classList.remove('show');
            messageInput.focus();
        });

        // Handle clear button
        clearButton.addEventListener('click', async () => {
            try {
                await fetch('/clear', { method: 'POST' });

                // Clear all messages except the first greeting and typing indicator
                const messages = chatMessages.querySelectorAll('.message');
                messages.forEach((msg, index) => {
                    if (index > 0) msg.remove();
                });
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        });

        // Focus input on page load
        messageInput.focus();
    </script>
</body>
</html>
"""

    # KEY CONCEPT: Define API endpoints with decorators
    # @app.route defines a URL path and what HTTP methods it accepts

    @app.route('/')
    def home():
        """Serve the chat interface HTML page"""
        return CHAT_HTML

    @app.route('/chat', methods=['POST'])
    def chat():
        """
        Main chat endpoint.
        Receives a message, sends it to Gemini, returns the response.
        """
        # KEY CONCEPT: Get JSON data from the request
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Please provide a message in JSON format: {"message": "your text"}'
            }), 400

        user_message = data['message']

        # Add user message to history
        conversation_history.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        try:
            # Send to Gemini
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=conversation_history,
            )

            ai_response = response.text if response.text else "I couldn't generate a response."

            # Add AI response to history
            conversation_history.append({
                "role": "model",
                "parts": [{"text": ai_response}]
            })

            # KEY CONCEPT: Return JSON response
            return jsonify({
                'response': ai_response,
                'message_count': len(conversation_history)
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/clear', methods=['POST'])
    def clear_history():
        """Clear conversation history"""
        conversation_history.clear()
        return jsonify({'message': 'Conversation history cleared'})

    # KEY CONCEPT: Run the Flask development server
    # debug=True enables auto-reload and better error messages
    # In production, you'd use a proper WSGI server like gunicorn
    print("\nStarting Flask server on http://localhost:5000")
    print("Open this URL in your browser to chat with Gemini!")
    app.run(debug=False, port=5000)


# =============================================================================
# MAIN MENU - Interactive exercise selector
# =============================================================================

def show_menu():
    """
    Displays the main menu and handles exercise selection.
    This is what runs when you execute the script.
    """
    # Dictionary mapping exercise numbers to their functions
    exercises = {
        '1': ('Simple Text Completion', exercise_1_simple_text_completion),
        '2': ('Chat Memory Simulation', exercise_2_chat_memory),
        '3': ('Generate Marketing Content', exercise_3_marketing_content),
        '4': ('Summarize a Web Page', exercise_4_summarize_webpage),
        '5': ('AI-Powered Code Reviewer', exercise_5_code_reviewer),
        '6': ('Multi-Modal Caption Generator', exercise_6_image_caption),
        '7': ('CSV Data Insights', exercise_7_csv_insights),
        '8': ('RAG-style Document Q&A', exercise_8_document_qa),
        '9': ('Emotion Analysis of Reviews', exercise_9_emotion_analysis),
        '10': ('Flask Chatbot API', exercise_10_flask_chatbot),
    }

    while True:
        # Display the menu
        print("\n" + "="*60)
        print("   PYTHON + GEMINI API: 10 PRACTICAL EXERCISES")
        print("="*60)
        print("\nChoose an exercise to run:\n")

        for num, (name, _) in exercises.items():
            print(f"  {num:>2}. {name}")

        print(f"\n   0. Exit")
        print("\n" + "="*60)

        # Get user choice
        choice = input("\nEnter exercise number (0-10): ").strip()

        if choice == '0':
            print("\nGoodbye! Happy coding! 🎉\n")
            break

        if choice in exercises:
            name, func = exercises[choice]
            try:
                # Run the selected exercise
                func()
            except KeyboardInterrupt:
                print("\n\nExercise interrupted.")
            except Exception as e:
                print(f"\nAn error occurred: {e}")

            # Wait before showing menu again
            input("\n\nPress Enter to return to menu...")
        else:
            print("\nInvalid choice. Please enter a number from 0 to 10.")


# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

# KEY CONCEPT: if __name__ == "__main__"
# This code only runs when the script is executed directly (not imported)
if __name__ == "__main__":
    # Check if API key is set
    if not API_KEY:
        print("="*60)
        print("ERROR: GOOGLE_API_KEY not found!")
        print("="*60)
        print("\nPlease create a .env file in this directory with:")
        print("GOOGLE_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        print("="*60)
    else:
        print("\n✓ API Key loaded successfully!")
        show_menu()