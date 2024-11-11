import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher

from dotenv import load_dotenv
load_dotenv()  # Automatically loads variables from .env file into environment

app = Flask(__name__)

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# Voice assistance function with enhanced topic management
conversation_history = []

def voice_assistance(user_input):
    global conversation_history

    # Improved prompt with focus on concise and direct answers
    prompt = f"""
    You are an AI assistant in an engaging conversation with a user. Refer to the converation history and user question below.
    
    ===Instructions
    Provide a direct and informative answer, focusing on the exact details the user is asking for. 
    Avoid unnecessary elaboration or asking follow-up questions unless essential to the user’s inquiry. 
    Keep the response clear, concise, and to the point. If the topic is complex, briefly summarize the key aspects.

    ===Conversation History
    {conversation_history}

    ===User Question
    {user_input}
    """

    response = model.generate_content(prompt).text

    # Update conversation history
    conversation_history.append({
        'user': user_input,
        'ai': response
    })

    return response


# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle voice input and return model response with conversation history
@app.route('/process_voice', methods=['POST'])
def process_voice():
    user_input = request.json.get("user_input")
    response = voice_assistance(user_input)

    # Return the updated conversation history
    return jsonify({'response': response, 'conversation_history': conversation_history})


if __name__ == '__main__':
    app.run(debug=True)