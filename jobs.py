# jobs.py

from printify_agent import PrintifyAgent

def run_daily_order_report():
    """Runs a daily order report."""
    agent = PrintifyAgent()
    agent.run_order_reporter(days=1)
    print("Successfully ran daily order report.")

def fulfill_pending_orders():
    """Fulfills all pending orders."""
    agent = PrintifyAgent()
    agent.run_order_fulfiller()
    print("Successfully fulfilled all pending orders.")

def run_inventory_sync():
    """Runs an inventory sync."""
    agent = PrintifyAgent()
    agent.run_inventory_sync()
    print("Successfully ran inventory sync.")
