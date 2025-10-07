# stripe_integration.py

import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

def create_checkout_session(design_id, price):
    """
    Creates a Stripe checkout session for a specific design.
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'NFT Mint for Design #{design_id}',
                        },
                        'unit_amount': price,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'http://localhost:8080/payment/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url='http://localhost:8080/payment/cancelled',
        )
        return checkout_session
    except Exception as e:
        return {"error": str(e)}
