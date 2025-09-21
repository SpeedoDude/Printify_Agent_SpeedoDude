# order_reporter.py

from api_clients import PrintifyApiClient
from collections import defaultdict

def run_order_reporter():
    """
    Fetches all completed orders and generates a sales report.
    """
    print("🤖 Order Reporter Agent: Initializing...")
    client = PrintifyApiClient()

    print("   - Fetching all completed orders...")
    orders_data = client.get_orders(status="fulfilled")

    if not orders_data or not orders_data.get('data'):
        print("No fulfilled orders found to report on.")
        return

    orders = orders_data['data']
    total_revenue = 0
    total_cost = 0
    product_sales = defaultdict(int)

    for order in orders:
        total_revenue += order.get('total_price', 0)
        total_cost += order.get('total_cost', 0)
        for item in order.get('line_items', []):
            title = item.get('metadata', {}).get('title', 'Unknown Product')
            quantity = item.get('quantity', 0)
            product_sales[title] += quantity

    total_profit = total_revenue - total_cost

    # --- Display Report ---
    print("\n--- 📈 Printify Sales Report ---")
    print(f"Total Orders Analyzed: {len(orders)}")
    print(f"Total Revenue: ${(total_revenue / 100):.2f}")
    print(f"Total Cost:    ${(total_cost / 100):.2f}")
    print(f"Gross Profit:  ${(total_profit / 100):.2f}")
    print("\n--- 👕 Top Selling Products ---")
    
    # Sort products by sales volume
    sorted_products = sorted(product_sales.items(), key=lambda item: item[1], reverse=True)
    
    for product, count in sorted_products[:10]: # Display top 10
        print(f"  - {product}: {count} units sold")
    print("---------------------------------")
