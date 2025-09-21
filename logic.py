# logic.py

import csv
import time
import os
from datetime import datetime, timedelta
from printify_client import get_request, post_request, SHOP_ID

# --- Order Reporting and Fulfillment Logic ---

def get_orders_report(days):
    """Fetches orders from the last X days and prints a summary."""
    past_date = datetime.now() - timedelta(days=days)
    print(f"Fetching orders since {past_date.strftime('%Y-%m-%d')}...")
    
    orders_data = get_request(f"/shops/{SHOP_ID}/orders.json")
    if not orders_data or 'data' not in orders_data:
        print("Could not retrieve orders.")
        return

    recent_orders = [
        order for order in orders_data['data']
        if datetime.fromisoformat(order['created_at'].replace('Z', '+00:00')) > past_date
    ]
    
    print(f"\n--- Found {len(recent_orders)} orders in the last {days} days ---")
    for order in recent_orders:
        print(f"  - Order #{order['id']}: Status '{order['status']}', Total: ${order['total_price']/100}")

def fulfill_pending_orders():
    """Finds 'on-hold' orders and sends them to production."""
    print("Checking for pending orders to fulfill...")
    orders_data = get_request(f"/shops/{SHOP_ID}/orders.json?status=on-hold")
    if not orders_data or 'data' not in orders_data:
        print("Could not retrieve orders or no pending orders found.")
        return

    pending_orders = orders_data['data']
    if not pending_orders:
        print("✅ No pending orders to fulfill.")
        return
        
    print(f"Found {len(pending_orders)} order(s) to fulfill.")
    for order in pending_orders:
        order_id = order['id']
        print(f"  - Fulfilling Order #{order_id}...")
        response = post_request(f"/shops/{SHOP_ID}/orders/{order_id}/send_to_production.json", {})
        if response:
            print(f"    ✅ Success! Order #{order_id} sent to production.")
        else:
            print(f"    ❌ Failed to send Order #{order_id} to production.")
        time.sleep(1) # Rate limit

# --- Bulk Product Creation Logic (Merged from bulk_creator.py) ---

def log_failed_job(log_file, data_row, error_message):
    """Appends failed job details to a CSV log file."""
    data_row['error'] = error_message
    file_exists = os.path.isfile(log_file)
    try:
        with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = data_row.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data_row)
    except Exception as e:
        print(f"CRITICAL LOGGING ERROR: Could not write to log file {log_file}. Reason: {e}")

def create_products_from_csv(file_path):
    """
    Reads product data from a CSV and creates products via the Printify API.
    Logs any failures to a separate file for retry.
    """
    print("🤖 Bulk Creator Logic: Initializing...")
    log_file_name = "failed_creation_jobs.csv"
    success_count = 0
    failure_count = 0

    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            if not rows:
                print("CSV file is empty or invalid.")
                return
            print(f"Found {len(rows)} products to create.")

            for index, row in enumerate(rows):
                title = row.get('title', 'No Title')
                print(f"\n--- Processing {index + 1}/{len(rows)}: '{title}' ---")

                try:
                    variants_str = row['variants_and_prices']
                    variants_payload = []
                    variant_ids_for_print_area = []
                    
                    for item in variants_str.split(','):
                        variant_id_str, price_str = item.split(':')
                        variant_id = int(variant_id_str)
                        price = int(price_str)
                        
                        variants_payload.append({
                            "id": variant_id,
                            "price": price,
                            "is_enabled": True
                        })
                        variant_ids_for_print_area.append(variant_id)

                    product_payload = {
                        "title": title,
                        "description": row['description'],
                        "blueprint_id": int(row['blueprint_id']),
                        "print_provider_id": int(row['print_provider_id']),
                        "variants": variants_payload,
                        "print_areas": [
                            {
                                "variant_ids": variant_ids_for_print_area,
                                "placeholders": [
                                    {
                                        "position": "front",
                                        "images": [{
                                            "id": row['image_id'],
                                            "x": 0.5, "y": 0.5, "scale": 1, "angle": 0
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                    
                    print("   - Sending data to Printify...")
                    response = post_request(endpoint=f"/shops/{SHOP_ID}/products.json", payload=product_payload)
                    
                    if response and 'id' in response:
                        print(f"   ✅ Success! Product '{response['title']}' created.")
                        success_count += 1
                    else:
                        raise Exception(f"API call failed. Response: {response}")

                except Exception as e:
                    error_message = str(e)
                    print(f"   ❌ FAILURE: {error_message}")
                    log_failed_job(log_file_name, row, error_message)
                    failure_count += 1
                
                time.sleep(1)

    except FileNotFoundError:
        print(f"🚨 Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected system-level error occurred: {e}")

    print("\n--- Bulk Creation Summary ---")
    print(f"Successful creations: {success_count}")
    print(f"Failed creations:     {failure_count}")
    if failure_count > 0:
        print(f"Details for failed jobs logged to '{log_file_name}'.")

