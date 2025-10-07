# subscriptions.py

SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free',
        'price': '$0/month',
        'features': [
            'Dashboard access',
            'Product management (up to 10 products)',
            'Order management (up to 20 orders)',
            'Limited SEO optimizations (3 per day)'
        ],
        'limits': {
            'products': 10,
            'orders': 20,
            'seo_optimizations': 3
        }
    },
    'pro': {
        'name': 'Pro',
        'price': '$29/month',
        'features': [
            'Everything in Free',
            'Unlimited products and orders',
            'Unlimited SEO optimizations',
            'Bulk product creator/updater',
            'AI Ad Generator'
        ],
        'limits': {
            'products': float('inf'),
            'orders': float('inf'),
            'seo_optimizations': float('inf')
        }
    },
    'business': {
        'name': 'Business',
        'price': '$99/month',
        'features': [
            'Everything in Pro',
            'Publish to all stores',
            'Automated error handling',
            'Priority support'
        ],
        'limits': {
            'products': float('inf'),
            'orders': float('inf'),
            'seo_optimizations': float('inf')
        }
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': '$299/month',
        'features': [
            'Everything in Business',
            'NFT Minting',
            'Dedicated account manager'
        ],
        'limits': {
            'products': float('inf'),
            'orders': float('inf'),
            'seo_optimizations': float('inf')
        }
    }
}

def has_access(user_tier, feature):
    """
    Checks if a user's subscription tier has access to a specific feature.
    """
    if feature == 'nft_minting':
        return user_tier == 'enterprise'
    if feature in ['bulk_creator', 'bulk_updater', 'ad_generator']:
        return user_tier in ['pro', 'business', 'enterprise']
    if feature in ['publish_to_all', 'auto_error_handling']:
        return user_tier in ['business', 'enterprise']
    return True # All tiers have access to basic features
