# civitai_client.py
import requests

BASE_URL = "https://civitai.com/api/v1"

class CivitaiClient:
    def __init__(self):
        self.base_url = BASE_URL

    def search_models(self, query: str, limit: int = 5):
        """
        Searches for models on Civitai.
        """
        endpoint = f"/models?query={query}&limit={limit}"
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while searching Civitai models: {e}")
            return []

    def get_model_version_info(self, version_id: int):
        """
        Gets information about a specific model version, which is needed for generation.
        """
        endpoint = f"/model-versions/{version_id}"
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while getting model version info: {e}")
            return None
