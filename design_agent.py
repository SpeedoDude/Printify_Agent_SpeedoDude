# design_agent.py

import replicate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

def generate_image_from_replicate(model_version, prompt, lora=None):
    """
    Generates an image from a text prompt using the Replicate API.
    """
    if not REPLICATE_API_TOKEN:
        return {"error": "Replicate API token is not configured on the server."}

    try:
        if lora:
            prompt = f"{prompt} <lora:{lora}:1>"
            
        output = replicate.run(
            model_version,
            input={"prompt": prompt}
        )
        return {"output": output}
    except Exception as e:
        print(f"An error occurred while contacting Replicate API: {e}")
        return {"error": "Failed to connect to the image generation service."}
