# main.py

from printify_agent import PrintifyAgent

def main():
    """
    Main function to initialize and run the Printify Agent.
    """
    agent = PrintifyAgent()

    # === CHOOSE THE TASK TO RUN ===
    # Comment/uncomment the tasks you want to perform.

    # 1. Generate an order report for the last 7 days
    # agent.run_order_reporter(days=7)

    # 2. Fulfill all pending orders
    # agent.run_order_fulfiller()

    # 3. Create products in bulk from a CSV file
    csv_file_path = "products_to_create.csv"
    agent.run_bulk_creator(file_path=csv_file_path)


if __name__ == "__main__":
    main()
