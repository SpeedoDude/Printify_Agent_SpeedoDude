# printify_client.py (Updated to use .env)

import requests
import os
import sys
from dotenv import load_dotenv

# --- Load Secrets from .env file ---
# This line looks for a .env file and loads its variables into the environment
load_dotenv() 

try:
    API_TOKEN = os.environ["PRINTIFY_API_TOKEN"]
    SHOP_ID = os.environ["PRINTIFY_SHOP_ID"]
except KeyError as e:
    # Exit gracefully if a required secret is not found.
    print(f"🚨 Critical Error: Environment variable not set: {e}")
    sys.exit("Please make sure your .env file exists and contains the required keys.")

# --- API Connection Details (No changes here) ---
BASE_URL = "https://api.printify.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# ... (The rest of the file: get_request, post_request, put_request functions remain exactly the same) ...


# --- API Connection Details ---
BASE_URL = "https://api.printify.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# --- Reusable API Request Functions ---
def get_request(endpoint):
    """Handles GET requests to the Printify API."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def post_request(endpoint, payload):
    """Handles POST requests to the Printify API."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        # Print more details if available from the response
        if e.response is not None:
            print(f"Error Response: {e.response.text}")
        return None
