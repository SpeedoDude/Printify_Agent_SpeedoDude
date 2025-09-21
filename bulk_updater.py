# bulk_updater.py (Upgraded with Error Logging)

import csv
import time
import math
import os # new import
from printify_client import get_request, put_request, SHOP_ID

# --- NEW: Error Logging Function ---
def log_failed_job(log_file, data_row, error_message):
    """Appends failed job details to a CSV log file."""
    # Add the error message to the row data for logging
    data_row['error'] = error_message
    
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(log_file)
    
    try:
        with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
            # Dynamically create fieldnames from the keys in the data row
            fieldnames = data_row.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data_row)
    except Exception as e:
        print(f"CRITICAL LOGGING ERROR: Could not write to log file {log_file}. Reason: {e}")

# --- Main function with modified try/except blocks ---
def update_products_from_csv(file_path):
    """
    Reads a CSV file to update product properties in bulk.
    Logs any failures to a separate file for retry.
    """
    print("🤖 Bulk Update Agent (with Error Logging): Initializing...")
    log_file_name = "failed_jobs_updater.csv"
    success_count = 0
    failure_count = 0

    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader) # Read all rows into memory to get total count
            print(f"Found {len(rows)} products to process.")

            for index, row in enumerate(rows):
                product_id = row.get('product_id')
                print(f"\n--- Processing {index + 1}/{len(rows)}: Product ID {product_id} ---")

                try:
                    if not product_id:
                        raise ValueError("product_id column is missing or empty")

                    # --- 1. Build the dynamic update payload ---
                    update_payload = {}
                    if row.get('title'):
                        update_payload['title'] = row['title']
                    if row.get('description'):
                        update_payload['description'] = row['description']

                    # --- 2. Handle Price Update Logic ---
                    new_price_str = row.get('price')
                    new_margin_str = row.get('margin')

                    if new_price_str:
                        # ... price calculation logic ...
                        new_price_int = int(new_price_str)
                        product_data = get_request(f"/shops/{SHOP_ID}/products/{product_id}.json")
                        if not product_data:
                            raise ConnectionError("Failed to fetch existing product data before price update.")
                        
                        variants_to_update = []
                        for variant in product_data['variants']:
                            variants_to_update.append({"id": variant['id'], "price": new_price_int})
                        update_payload['variants'] = variants_to_update
                        print(f"   - Staging direct price update: ${new_price_int / 100:.2f}")

                    elif new_margin_str:
                        # ... margin calculation logic ...
                        margin_decimal = float(new_margin_str) / 100.0
                        if margin_decimal < 0 or margin_decimal >= 1:
                            raise ValueError(f"Invalid margin '{new_margin_str}%. Must be between 0 and 99.")
                        
                        product_data = get_request(f"/shops/{SHOP_ID}/products/{product_id}.json")
                        if not product_data:
                            raise ConnectionError("Failed to fetch existing product data before margin calculation.")

                        variants_to_update = []
                        for variant in product_data['variants']:
                            variant_cost = variant['cost']
                            calculated_price = math.ceil(variant_cost / (1 - margin_decimal))
                            variants_to_update.append({"id": variant['id'], "price": int(calculated_price)})
                        update_payload['variants'] = variants_to_update
                        print(f"   - Staging margin-based price update ({new_margin_str}%)")

                    # --- 3. Send update request ---
                    if update_payload:
                        endpoint = f"/shops/{SHOP_ID}/products/{product_id}.json"
                        response = put_request(endpoint, update_payload)
                        if response:
                            print(f"   ✅ Success! Product {product_id} updated.")
                            success_count += 1
                        else:
                            raise ConnectionError("API call failed. Response was negative.")
                    else:
                        print("   - No changes specified. Skipping.")
                        success_count += 1 # Count as success if no action needed

                except Exception as e:
                    # --- CATCH FAILURE AND LOG IT ---
                    error_message = str(e)
                    print(f"   ❌ FAILURE: {error_message}")
                    log_failed_job(log_file_name, row, error_message)
                    failure_count += 1
                
                time.sleep(1) # Rate limiting

    except FileNotFoundError:
        print(f"🚨 Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected system-level error occurred: {e}")

    print("\n--- Bulk Update Summary ---")
    print(f"Successful operations: {success_count}")
    print(f"Failed operations:     {failure_count}")
    if failure_count > 0:
        print(f"Details for failed jobs logged to '{log_file_name}'.")

# --- Refactor main execution block for importability ---
def run_bulk_updater():
    csv_file_name = "products_to_update.csv"
    update_products_from_csv(csv_file_name)

if __name__ == "__main__":
    run_bulk_updater()
