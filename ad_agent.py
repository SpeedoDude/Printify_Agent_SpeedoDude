# ad_agent.py

from printify_client import PrintifyClient
from logic import get_gemini_vision_pro_model  # Reusing the Gemini logic

def generate_ad_copy(product_id: str, platform: str):
    """
    Generates ad copy for a specific product and platform using an AI model.
    """
    printify_client = PrintifyClient()
    product_data = printify_client.get_product(product_id)

    if not product_data:
        return {"error": "Could not retrieve product data from Printify."}

    image_url = product_data.get("images", [{}])[0].get("src")
    if not image_url:
        return {"error": "Product has no image to analyze."}

    # AI Prompt tailored for ad copy
    prompt = f"""
    Based on the following product information and image, generate compelling ad copy for the '{platform}' platform.

    Product Title: {product_data.get('title')}
    Product Description: {product_data.get('description')}

    Ad copy requirements for {platform}:
    - Headline: A short, catchy title.
    - Body: A persuasive and engaging description. Keep it concise and highlight key benefits.
    - Call to Action (CTA): A clear and strong call to action.

    Return the response as a JSON object with the keys "headline", "body", and "cta".
    """

    try:
        model = get_gemini_vision_pro_model()
        response = model.generate_content([prompt, {"url": image_url}])
        
        # Extracting and parsing the JSON from the response
        import json
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        ad_copy = json.loads(clean_response)
        
        return ad_copy

    except Exception as e:
        print(f"An error occurred while generating ad copy: {e}")
        return {"error": f"Failed to generate ad copy. Raw response: {str(e)}"}
