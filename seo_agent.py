# seo_agent.py
import json
from api_clients import PrintifyApiClient, GeminiApiClient # Assuming GeminiApiClient can handle images

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
    
    # NOTE: This assumes your GeminiApiClient is updated to handle multimodal input.
    # The actual method might differ based on the library you are using.
    generated_text = gemini_client.generate_content_with_image(prompt, image_url)
    return generated_text


def run_seo_optimizer(product_id: str):
    """
    Fetches a product and its image, generates new SEO content with AI, and updates it.
    """
    print(f"🤖 SEO Optimizer Agent: Initializing for product {product_id}...")
    printify_client = PrintifyApiClient()
    gemini_client = GeminiApiClient()

    # 1. Fetch the product from Printify
    print("   - Fetching product data from Printify...")
    product = printify_client.get_product(product_id)
    if not product:
        print(f"❌ Could not retrieve product with ID: {product_id}")
        return

    original_title = product.get("title", "")
    
    # --- NEW: Extract the main image URL ---
    try:
        image_url = product["images"][0]["src"]
        print(f"   - Found product: '{original_title}'")
        print(f"   - Found image URL: {image_url}")
    except (IndexError, KeyError):
        print(f"❌ Product '{original_title}' has no images. Aborting.")
        return
    # --- END NEW ---

    # 2. Generate new content with Gemini using the image
    print("   - Asking Gemini AI to analyze the product image...")
    ai_response_text = generate_seo_content_from_image(gemini_client, original_title, image_url)
    # ... (the rest of the function for parsing JSON and updating Printify remains the same)

    # 3. Parse the AI-generated JSON response
    try:
        if "```json" in ai_response_text:
            ai_response_text = ai_response_text.split("```json")[1].split("```")[0].strip()
            
        data = json.loads(ai_response_text)
        new_title = data["new_title"]
        new_description = data["new_description"]
        print(f"   - AI Generated Title: '{new_title}'")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Failed to parse the AI JSON response. Error: {e}")
        print(f"   - Raw Response From AI: {ai_response_text}")
        return

    # 4. Update the product on Printify
    update_payload = {
        "title": new_title,
        "description": new_description
    }
    
    print("   - Sending updated data back to Printify...")
    response = printify_client.update_product(product_id, update_payload)
    if response:
        print("✅ Success! Product SEO has been updated based on its design.")
    else:
        print("❌ Failure. Could not update the product on Printify.")

