import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
# Replace these variables with your actual values
SUBDOMAIN = os.getenv("SUBDOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
email_address = "tangbaohuy2307@gmail.com"

# Token URL
token_url = f"https://{SUBDOMAIN}.zendesk.com/api/v2/oauth/tokens"

# Data to be sent in the request
data = {
    "token": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scopes": ["tickets:read"]
    }
}

# Authorization configuration
credentials = f"{email_address}/token:{ZENDESK_API_TOKEN}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# Headers configuration
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}

# Function to create access token
def create_token():
    # Make a POST request to get the OAuth access token
    response = requests.post(token_url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        token_data = response.json()
        token_id = token_data["token"]["id"]
        access_token = token_data["token"]["token"]
        response = f"Token successfully created: {token_id}"
        print(response)
        return access_token
    elif response.status_code == 204:
        print("Successfully requested but no content returned")
        return None
    else:
        print(f"Failed to create new access token: {response.status_code}")
        print(response.text)
        return None
    
# Function to show a specific access token
def show_token(token_id):
    # Make a GET request to show the OAuth access token
    response = requests.get(token_url + f"/{token_id}", json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        token_data = response.json()
        token_details = token_data["token"]
        print(f"Token {token_id}:\n{token_details}")
        return token_details
    else:
        print(f"Failed to show token {token_id}: {response.status_code}")
        print(response.text)
        return None
    
# Function to list out all the OAuth access tokens available
def list_tokens():
    # Make a GET request to get a list of all OAuth access tokens
    response = requests.get(token_url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        token_data = response.json()
        print(token_data)
        return token_data
    else:
        print(f"Failed to access the list of all tokens: {response.status_code}")
        print(response.text)
        return None
    
# Function to delete an OAuth access token
def revoke_token(token_id):
    # Make a DELETE request to get a list of all OAuth access tokens
    response = requests.delete(token_url + f"/{token_id}", json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200 or response.status_code == 204:
        response = f"Token {token_id} successfully deleted"
        print(response)
        return response
    else:
        print(f"Failed to delete token {token_id}: {response.status_code}")
        print(response.text)
        return None