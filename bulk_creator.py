# bulk_creator.py (Upgraded with Error Logging)

import csv
import time
import os
from printify_client import post_request, SHOP_ID

# --- NEW: Error Logging Function ---
def log_failed_job(log_file, data_row, error_message):
    """Appends failed job details to a CSV log file."""
    # Add the error message to the row data for logging
    data_row['error'] = error_message
    
    # Check if file exists to determine if we need to write headers
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

# --- Main function with modified try/except blocks ---
def create_products_from_csv(file_path):
    """
    Reads product data from a CSV file and creates each product via the Printify API.
    Logs any failures to a separate file for retry.
    """
    print("🤖 Bulk Creator Agent (with Error Logging): Initializing...")
    log_file_name = "failed_creation_jobs.csv"
    success_count = 0
    failure_count = 0

    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            print(f"Found {len(rows)} products to create.")

            for index, row in enumerate(reader):
                title = row['title']
                print(f"\n--- Processing {index + 1}/{len(rows)}: '{title}' ---")

                try:
                    # --- 1. Parse variants and prices ---
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

                    # --- 2. Construct the full API payload ---
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
                    
                    # --- 3. Send the request to Printify ---
                    print("   - Sending data to Printify...")
                    response = post_request(endpoint=f"/shops/{SHOP_ID}/products.json", payload=product_payload)
                    
                    if response:
                        print(f"   ✅ Success! Product '{response['title']}' created.")
                        success_count += 1
                    else:
                        raise Exception("API call failed, returned no response or negative status.")

                except Exception as e:
                    # --- CATCH FAILURE AND LOG IT ---
                    error_message = str(e)
                    print(f"   ❌ FAILURE: {error_message}")
                    log_failed_job(log_file_name, row, error_message)
                    failure_count += 1
                
                time.sleep(1) # Rate limit between product creations

    except FileNotFoundError:
        print(f"🚨 Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected system-level error occurred: {e}")

    print("\n--- Bulk Creation Summary ---")
    print(f"Successful creations: {success_count}")
    print(f"Failed creations:     {failure_count}")
    if failure_count > 0:
        print(f"Details for failed jobs logged to '{log_file_name}'.")

# --- Refactor main execution block for importability ---
def run_bulk_creator():
    csv_file_name = "products_to_create.csv"
    create_products_from_csv(csv_file_name)

if __name__ == "__main__":
    run_bulk_creator()
