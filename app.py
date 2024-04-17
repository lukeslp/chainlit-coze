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

    # Step 1: Retrieve the current chat history
    @cl.step
    def retrieve_chat_history():
        chat_history = cl.user_session.get('chat_history', [])
        return chat_history

    chat_history = retrieve_chat_history()

    # Step 2: Append the user's message to the chat history
    @cl.step
    def append_user_message(chat_history, message):
        chat_history.append(
            {"role": "user", "content": message.content, "content_type": "text"})
        return chat_history

    chat_history = append_user_message(chat_history, message)

    # Step 3: Create the data payload for the API request
    @cl.step
    def create_data_payload(chat_history):
        data = {
            'bot_id': COZE_BOT_ID,
            'user': 'chainlit_user',  # This can be a unique identifier for the user
            'query': message.content,
            'chat_history': chat_history,
            'stream': True  # Assuming we want to use streaming responses
        }
        return data

    data = create_data_payload(chat_history)

    # Step 4: Make a post request to the Coze API
    @cl.step
    def make_api_request(data):
        response = requests.post(
            COZE_API_ENDPOINT, headers=headers, json=data, stream=True)
        return response

    response = make_api_request(data)

    # If the response is successful, process and display it
    if response.status_code == 200:

        # Step 5: Handle streaming response
        @cl.step
        async def stream_step():
            # Initialize an empty string to accumulate message content
            coze_message = ""
            # Create a Chainlit Message object for streaming
            stream_message = cl.Message(content="")
            await stream_message.send()
            # Parse the streaming response
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if 'data:' in decoded_line:
                        message_data = decoded_line.split('data:', 1)[
                            1].strip()
                        message_json = json.loads(message_data)
                        if message_json.get('event') == 'message':
                            # Check if the message is of type 'answer' and accumulate the content
                            if message_json['message']['type'] == 'answer':
                                coze_message += message_json['message']['content']
                                # Update the content of the stream_messagexq
                                stream_message.content = coze_message
                                await stream_message.update()
                            # Check if the message is finished
                            if message_json.get('is_finish', False):
                                # If the message is complete, update the chat history
                                chat_history.append(
                                    {"role": "assistant", "content": coze_message, "content_type": "text"})
                                cl.user_session.set(
                                    'chat_history', chat_history)
                        elif message_json.get('event') == 'error':
                            # If an error event is received, check if it's a token quota error
                            error_info = message_json.get(
                                'error_information', {})
                            if error_info.get('err_code') == 702232007:
                                # If it's a token quota error, send an appropriate message to the UI
                                quota_error_message = "Sorry, the token quota has been used up. Please check your balance or contact Coze support for assistance."
                                await cl.Message(content=quota_error_message).send()
                            break
                        elif message_json.get('event') == 'done':
                            # If the 'done' event is received, break the loop
                            break

        # Call the streaming step
        await stream_step()
    else:
        # If there's an error, send an error message to the UI
        error_message = f"An error occurred: {response.status_code}"
        await cl.Message(content=error_message).send()

# Run the chatbot application
if __name__ == '__main__':
    cl.run()
