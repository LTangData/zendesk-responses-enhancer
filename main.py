import os
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Set your OpenAI API key
openai = OpenAI(api_key=OPENAI_API_KEY)

# Pydantic model for the request body
class BotRequest(BaseModel):
    question: str
    tag: str

# Define a dictionary to map tags to details
tag_details = {
    'payment': "Make sure to inform the user about the accepted payment methods: credit cards, PayPal, and wire transfer. Also, mention that the payment must be completed within 7 days of placing the order.",
    'refund': "Inform the user that refunds can be requested within 30 days of purchase, and they must provide the order number. Refunds are processed within 5-7 business days.",
    # Add more tags and their associated details as needed
}

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
async def webhook(bot_request: BotRequest):
    # Extract the user's question and the associated tag from the request
    user_question = bot_request.question
    tag = bot_request.tag
    
    # Generate a response using GPT-4o mini
    response_text = generate_response(user_question, tag)
    
    # Return the generated response back to the bot
    return response_text

