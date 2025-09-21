# printify_agent.py

from logic import get_orders_report, fulfill_pending_orders, create_products_from_csv

class PrintifyAgent:
    """An agent to automate Printify store tasks."""
    def __init__(self):
        print("🤖 Printify Agent initialized.")

    def run_order_reporter(self, days):
        """Generates a report of recent orders."""
        print("\n--- Running Order Reporter ---")
        get_orders_report(days)

    def run_order_fulfiller(self):
        """Fulfills all pending orders."""
        print("\n--- Running Order Fulfiller ---")
        fulfill_pending_orders()

    def run_bulk_creator(self, file_path):
        """
        Triggers the bulk product creation process using a CSV file.
        """
        print("\n--- Running Bulk Product Creator ---")
        create_products_from_csv(file_path)

