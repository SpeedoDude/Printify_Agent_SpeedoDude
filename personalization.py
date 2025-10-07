# personalization.py

from user_activity import UserActivity

RECOMMENDATIONS = {
    'dashboard': "Welcome back! Check out the latest orders or see any failed jobs.",
    'products': "Manage your inventory by viewing or updating your products.",
    'orders': "Review your recent orders and fulfill any that are on-hold.",
    'seo_optimizer': "Improve your product visibility with our AI-Powered SEO Agent.",
    'bulk_creator': "Save time by creating products in bulk from a CSV file.",
    'bulk_updater': "Update multiple products at once with our bulk updater.",
    'inventory': "Check for out-of-stock products to keep your store running smoothly.",
    'catalog': "Explore the Printify catalog to find new products for your store.",
    'financials': "Get an overview of your store's financial performance.",
    'customers': "View your customer list and their order history.",
    'marketing': "Create email campaigns and discount codes to boost your sales.",
    'ad_generator': "Generate compelling ad copy for your products with our AI Ad Generator.",
    'publish_to_all': "Publish a product to all your stores with a single click.",
    'community': "Engage with your customers through reviews, contests, and referrals.",
    'design_studio': "Create your own unique designs and mint them as NFTs.",
    'nft_minting': "Mint your designs as NFTs on the blockchain.",
    'legal_dashboard': "Check your products for copyright and trademark issues.",
    'robo_script_automator': "Automate UI testing and other repetitive tasks with Robo scripts.",
    'settings': "Manage your API keys and other application settings."
}

class Personalization:
    def __init__(self):
        self.activity_db = UserActivity()

    def get_recommendations(self, username):
        """Generates personalized recommendations for a user."""
        user_activity = self.activity_db.get_user_activity(username)
        recommendations = []

        if not user_activity:
            return ["Welcome! Start by exploring the dashboard or adding your first product."]

        # Suggest exploring unused features
        used_features = user_activity.get('features_used', {}).keys()
        for feature, recommendation in RECOMMENDATIONS.items():
            if feature not in used_features:
                recommendations.append(f"New to you: {recommendation}")
                if len(recommendations) >= 3:
                    return recommendations
        
        # If all features used, provide general tips
        if not recommendations:
            recommendations.append("You're a power user! Have you tried automating tasks with the Robo Automator?")
            recommendations.append("Keep your SEO fresh by running the optimizer on older products.")
        
        return recommendations
