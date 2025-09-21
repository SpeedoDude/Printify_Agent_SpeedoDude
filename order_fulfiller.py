# order_fulfiller.py

import time
from api_clients import PrintifyApiClient

def run_order_fulfiller():
    """
    Finds all 'on-hold' orders and sends them to production.
    """
    print("🤖 Order Fulfillment Agent: Initializing...")
    client = PrintifyApiClient()

    print("   - Searching for orders with status 'on-hold'...")
    orders_data = client.get_orders(status="on-hold")
    
    if not orders_data or not orders_data.get('data'):
        print("✅ No 'on-hold' orders found.")
        return
        
    on_hold_orders = orders_data['data']
    print(f"   - Found {len(on_hold_orders)} orders to fulfill.")

    for order in on_hold_orders:
        order_id = order['id']
        created_at = order['created_at']
        print(f"\n   -> Fulfilling Order ID: {order_id} (Created: {created_at})")
        
        response = client.send_to_production(order_id)
        if response:
            print(f"      ✅ Success! Order {order_id} sent to production.")
        else:
            print(f"      ❌ Failed to send order {order_id} to production.")
        
        time.sleep(1) # Rate limit between actions
