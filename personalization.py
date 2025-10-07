# personalization.py

from user_activity import UserActivity
from logic import get_gemini_vision_pro_model
import random

class Personalization:
    def __init__(self):
        self.activity_db = UserActivity()
        # In a real application, you would have a database of products and orders
        self.products = {
            "p1": {"name": "T-Shirt", "category": "Apparel"},
            "p2": {"name": "Mug", "category": "Home Goods"},
            "p3": {"name": "Hoodie", "category": "Apparel"},
            "p4": {"name": "Phone Case", "category": "Accessories"},
            "p5": {"name": "Sticker", "category": "Accessories"},
        }
        self.orders = {
            "user1": ["p1", "p3"],
            "user2": ["p2", "p5"],
        }

    def get_recommendations(self, username):
        """
        Generates personalized product recommendations for a user based on their order history.
        """
        user_orders = self.orders.get(username, [])
        if not user_orders:
            # For new users, recommend a few random popular products
            recommended_products = random.sample(list(self.products.values()), 3)
            return {"products": recommended_products}

        # Find categories the user has purchased from
        purchased_categories = {self.products[p_id]["category"] for p_id in user_orders}
        
        # Recommend other products from the same categories
        recommendations = []
        for p_id, product in self.products.items():
            if p_id not in user_orders and product["category"] in purchased_categories:
                recommendations.append(product)
        
        # If not enough recommendations, add some random popular products
        if len(recommendations) < 3:
            for p_id, product in self.products.items():
                if product not in recommendations and p_id not in user_orders:
                    recommendations.append(product)
                    if len(recommendations) >= 3:
                        break

        return {"products": recommendations[:3]}

    def generate_personalized_marketing_message(self, username):
        """
        Generates a personalized marketing message for a user using an AI model.
        """
        user_orders = self.orders.get(username, [])
        if not user_orders:
            return "Check out our new arrivals and find your next favorite product!"

        # Get the names of the products the user has ordered
        ordered_product_names = [self.products[p_id]["name"] for p_id in user_orders]

        try:
            model = get_gemini_vision_pro_model()
            prompt = f"""
            Generate a short, friendly, and personalized marketing message for a user.
            The user has previously purchased the following items: {', '.join(ordered_product_names)}.
            Suggest a new product or category they might like.

            Return the response as a JSON object with a "message" key.
            """
            response = model.generate_content([prompt])
            
            import json
            clean_response = response.text.strip().replace("```json", "").replace("```", "")
            message_data = json.loads(clean_response)
            
            return message_data.get("message")
        except Exception as e:
            print(f"An error occurred while generating personalized message: {e}")
            return f"Because you liked {', '.join(ordered_product_names)}, you might also love our new collection of accessories!"
