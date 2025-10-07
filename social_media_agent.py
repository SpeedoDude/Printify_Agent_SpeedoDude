# social_media_agent.py

from logic import get_gemini_vision_pro_model
import os

# In a real application, you would use libraries like 'facebook-sdk' or 'tweepy'
# to interact with social media APIs. For now, we'll simulate this.

class SocialMediaAgent:
    def __init__(self):
        self.platforms = ["Facebook", "Twitter", "Instagram"]

    def generate_ad_copy(self, product_name, product_description):
        """
        Generates compelling ad copy for a product using an AI model.
        """
        try:
            model = get_gemini_vision_pro_model()
            prompt = f"""
            Generate a short, engaging social media post to promote a new product.
            The post should be exciting and encourage users to check out the product.

            Product Name: "{product_name}"
            Description: "{product_description}"

            Return the response as a JSON object with a "ad_copy" key.
            """
            response = model.generate_content([prompt])
            
            import json
            clean_response = response.text.strip().replace("```json", "").replace("```", "")
            ad_copy_data = json.loads(clean_response)
            
            return ad_copy_data.get("ad_copy")
        except Exception as e:
            print(f"An error occurred while generating ad copy: {e}")
            return f"Check out our new product: {product_name}! {product_description}"

    def post_to_social_media(self, product_name, product_description, image_url):
        """
        Posts a new product to all connected social media platforms.
        """
        ad_copy = self.generate_ad_copy(product_name, product_description)
        
        # Simulate posting to social media
        print(f"--- Posting to Social Media ---")
        for platform in self.platforms:
            print(f"Platform: {platform}")
            print(f"Ad Copy: {ad_copy}")
            print(f"Image URL: {image_url}")
            print(f"Status: Posted successfully")
            print(f"---------------------------------")
            
        return {"status": "success", "message": f"Successfully posted '{product_name}' to all platforms."}

    def get_connected_platforms(self):
        """
        Returns a list of social media platforms the user has connected.
        (This would be loaded from user settings in a real app).
        """
        return self.platforms
