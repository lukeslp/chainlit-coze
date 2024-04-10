import os
import requests
import json
import chainlit as cl
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Coze API key and bot ID from environment
COZE_API_KEY = os.getenv('COZE_API_KEY')
COZE_BOT_ID = os.getenv('COZE_BOT_ID')

# Coze API endpoint for chat completions
COZE_API_ENDPOINT = 'https://api.coze.com/open_api/v2/chat'

# Set up the headers for the HTTP requests to the Coze API
headers = {
    'Authorization': f'Bearer {COZE_API_KEY}',
    'Content-Type': 'application/json'
}

# Function called at the start of the chat, setting up chat settings


@cl.on_chat_start
async def start():
    # Initialize the user session with default values
    cl.user_session.set('chat_history', [])

# Function to handle incoming messages from the user


@cl.on_message
async def coze_chat(message: cl.Message):
    # Retrieve the current chat history
    chat_history = cl.user_session.get('chat_history', [])

    # Append the user's message to the chat history
    chat_history.append(
        {"role": "user", "content": message.content, "content_type": "text"})

    # Create the data payload for the API request
    data = {
        'bot_id': COZE_BOT_ID,
        'user': 'chainlit_user',  # This can be a unique identifier for the user
        'query': message.content,
        'chat_history': chat_history,
        'stream': True  # Assuming we want to use streaming responses
    }

    # Make a post request to the Coze API
    response = requests.post(COZE_API_ENDPOINT, headers=headers, json=data)

    # If the response is successful, process and display it
    if response.status_code == 200:
        # Parse the streaming response
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if 'data:' in decoded_line:
                    message_data = decoded_line.split('data:', 1)[1].strip()
                    message_json = json.loads(message_data)
                    if message_json.get('event') == 'message':
                        # Extract the message content and update the chat history
                        coze_message = message_json['message']['content']
                        chat_history.append(message_json['message'])
                        cl.user_session.set('chat_history', chat_history)
                        # Send the message to the UI
                        await cl.Message(content=coze_message).send()
                    elif message_json.get('event') == 'done':
                        break
    else:
        # If there's an error, log it and send an error message to the UI
        error_message = f"An error occurred: {response.status_code}"
        await cl.Message(content=error_message).send()

# Run the chatbot application
if __name__ == '__main__':
    cl.run()
