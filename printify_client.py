# printify_client.py

import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

try:
    API_TOKEN = os.environ["PRINTIFY_API_TOKEN"]
except KeyError as e:
    print(f"🚨 Critical Error: Environment variable not set: {e}")
    sys.exit("Please make sure your .env file exists and contains the required keys.")

BASE_URL = "https://api.printify.com/v1"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

class PrintifyClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS

    def _get_request(self, endpoint):
        """Handles GET requests to the Printify API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def _post_request(self, endpoint, payload):
        """Handles POST requests to the Printify API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            if e.response is not None:
                print(f"Error Response: {e.response.text}")
            return None
            
    def get_shops(self):
        """Retrieves a list of all shops."""
        return self._get_request("/shops.json")

    def get_products(self, shop_id):
        """Retrieves a list of all products in a specific shop."""
        return self._get_request(f"/shops/{shop_id}/products.json")

    def get_product(self, shop_id, product_id):
        """Retrieves a specific product."""
        return self._get_request(f"/shops/{shop_id}/products/{product_id}.json")

    def publish_product(self, shop_id, product_id):
        """Publishes a product to a specific shop."""
        return self._post_request(f"/shops/{shop_id}/products/{product_id}/publish.json", {"title": True, "description": True, "images": True, "variants": True, "tags": True})
        
    def unpublish_product(self, shop_id, product_id):
        """Unpublishes a product from a specific shop."""
        return self._post_request(f"/shops/{shop_id}/products/{product_id}/unpublish.json", {})

    def get_publication_status(self, shop_id, product_id):
        """Checks the publication status of a product."""
        product_data = self.get_product(shop_id, product_id)
        if product_data:
            return product_data.get("publication", {}).get("status")
        return None
