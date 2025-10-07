# design_agent.py

import replicate
import os
from dotenv import load_dotenv
from logic import get_gemini_vision_pro_model
import openai  # Import the OpenAI library

# Load environment variables
load_dotenv()
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # Make sure to set this in your .env file

# Configure the OpenAI client
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

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

def generate_ai_design(prompt: str):
    """
    Generates a new, more creative design prompt using Gemini and then creates an image with DALL-E 3.
    """
    if not OPENAI_API_KEY:
        return {"error": "OpenAI API key is not configured on the server."}

    try:
        # Step 1: Use Gemini to brainstorm a more creative prompt for DALL-E 3
        model = get_gemini_vision_pro_model()
        creative_prompt_response = model.generate_content([f"""
            Analyze the following user prompt and generate a more detailed and creative prompt for DALL-E 3.
            The new prompt should be optimized to generate a visually stunning and unique design for a t-shirt.
            Focus on extracting key elements and adding artistic flair.

            User Prompt: "{prompt}"

            Return the response as a JSON object with a "dalle_prompt" key.
        """])

        import json
        clean_response = creative_prompt_response.text.strip().replace("```json", "").replace("```", "")
        dalle_prompt_data = json.loads(clean_response)
        dalle_prompt = dalle_prompt_data.get("dalle_prompt")

        if not dalle_prompt:
            return {"error": "Could not generate a creative prompt from your input."}

        # Step 2: Use the new prompt to generate an image with DALL-E 3
        response = openai.Image.create(
            model="dall-e-3",
            prompt=dalle_prompt,
            n=1,
            size="1024x1024",
            quality="standard",
        )
        
        image_url = response.data[0].url
        return {"output": [image_url]} # Keep the output format consistent
        
    except Exception as e:
        print(f"An error occurred during AI design generation: {e}")
        return {"error": f"Failed to generate AI design. Raw response: {str(e)}"}
