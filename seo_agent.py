# seo_agent.py
import json
from api_clients import PrintifyApiClient, GeminiApiClient

def generate_seo_content_from_image(gemini_client, product_title, image_url):
    """
    Generates SEO content by having the AI analyze the product image.
    """
    prompt = f"""
    You are an expert SEO copywriter for an e-commerce print-on-demand store.
    Your primary task is to analyze the provided product image and generate a compelling, SEO-optimized title and description. The current title is "{product_title}" for context.

    **Instructions:**
    1.  **Analyze the Image:** Look closely at the design, colors, style, and subject matter in the image.
    2.  **Generate a new title:** Create a descriptive and engaging title (100-120 characters) that captures the essence of the visual design.
    3.  **Write a new product description:** Write an HTML description (600-700 characters) that vividly describes the artwork. Mention the colors, the mood, potential themes (e.g., retro, minimalist, abstract), and who might love this design. End with a call-to-action.
    
    **CRITICAL:** Return your response as a valid JSON object, and nothing else.
    The JSON object must have two keys: "new_title" (string) and "new_description" (string).
    """
    
    generated_text = gemini_client.generate_content_with_image(prompt, image_url)
    return generated_text

def run_seo_optimizer(product_id: str):
    """
    Fetches a product and its image, then generates new SEO content with AI.
    Returns a dictionary with original and new content, or an error message.
    """
    printify_client = PrintifyApiClient()
    gemini_client = GeminiApiClient()

    # 1. Fetch the product from Printify
    product = printify_client.get_product(product_id)
    if not product:
        return {"error": f"Could not retrieve product with ID: {product_id}"}

    original_title = product.get("title", "")
    original_description = product.get("description", "")
    
    try:
        image_url = product["images"][0]["src"]
    except (IndexError, KeyError):
        return {"error": f"Product '{original_title}' has no images. Aborting."}

    # 2. Generate new content with Gemini using the image
    ai_response_text = generate_seo_content_from_image(gemini_client, original_title, image_url)
    
    # 3. Parse the AI-generated JSON response
    try:
        if "```json" in ai_response_text:
            ai_response_text = ai_response_text.split("```json")[1].split("```")[0].strip()
            
        data = json.loads(ai_response_text)
        new_title = data["new_title"]
        new_description = data["new_description"]
    except (json.JSONDecodeError, KeyError) as e:
        return {"error": f"Failed to parse the AI JSON response. Error: {e}", "raw_response": ai_response_text}

    return {
        "original_title": original_title,
        "original_description": original_description,
        "image_url": image_url,
        "new_title": new_title,
        "new_description": new_description
    }

def update_product_seo(product_id: str, new_title: str, new_description: str):
    """
    Updates the product's title and description on Printify.
    """
    printify_client = PrintifyApiClient()
    update_payload = {
        "title": new_title,
        "description": new_description
    }
    
    response = printify_client.update_product(product_id, update_payload)
    if response:
        return {"success": True, "message": "Product SEO has been updated successfully."}
    else:
        return {"success": False, "message": "Failed to update the product on Printify."}
