import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from models import *

# Import all environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Make sure this is correctly set in your environment
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN") # Make sure this is correctly set in your environment
ZENDESK_SUBDOMAIN = "comany1205" # Replace with your Zendesk subdomain
ZENDESK_USER_MAIL = "tangbaohuy2307@gmail.com" # Replace with the Zendesk email address used to access the subdomain

# Check if OPENAI_API_KEY and ZENDESK_API_TOKEN were correctly retrieved from environment
if not OPENAI_API_KEY:
    print("OPENAI_API_KEY environment variable is not set. Exiting.")
    exit()
elif not ZENDESK_API_TOKEN:
    print("ZENDESK_API_TOKEN environment variable is not set. Exiting.")
    exit()

# Create an instance of FastAPI application
app = FastAPI()

# Call the OpenAI API using your key
openai = OpenAI(api_key=OPENAI_API_KEY)

# Define a dictionary to map tags to details
tag_details = {
    "payment": "Make sure to inform the user about the accepted payment methods: credit cards, PayPal, and wire transfer. Also, mention that the payment must be completed within 7 days of placing the order.",
    "refund": "Inform the user that refunds can be requested within 30 days of purchase, and they must provide the order number. Refunds are processed within 5-7 business days.",
    # Add more tags and their associated details as needed
}

# Function to extract the question input by user and its tag
def get_question_and_tag(chat_id):
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/chat/chats/{chat_id}"
    headers = {
        "Content-Type": "application/json"
    }
    auth = f"{ZENDESK_USER_MAIL}/token", ZENDESK_API_TOKEN

    # Perform the HTTP GET request
    response = requests.get(url, auth=auth, headers=headers)

    print(chat_id)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, "Problem with the request. Exiting.")
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    print(data)

    return

# Function to generate a prompt and get a response from GPT
def generate_response(user_question: str, tag: str) -> str:
    # Retrieve the details based on the tag
    details = tag_details.get(tag.lower(), "No specific details available for this tag.")
    
    # Create a prompt by combining the user question and the relevant details
    prompt = f"User asked: {user_question}. Please include the following information in your response: {details}"
    
    # Call GPT-40 mini to generate a response
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract the generated response text
    content = response.choices[0].message.content

    print(content)

    # Return the generated response text
    return {"response": content}

# Webhook endpoint to handle incoming requests from the Zendesk bot
@app.post("/webhook")
async def webhook(user_request: UserRequest):
    # Extract the user's question and the associated tag from the chat using chat id
    chat_id = user_request.chat_id
    request_details = get_question_and_tag(chat_id)
    
    user_question = request_details.question
    tag = request_details.tag

    # Generate a response using GPT-4o mini
    response_text = generate_response(user_question, tag)
    
    # Return the generated response back to the bot
    return response_text