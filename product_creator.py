# product_creator.py

import csv
import time
from api_clients import PrintifyApiClient
from jobs_manager import FailedJobsManager

def run_bulk_creator(file_path: str):
    """
    Reads product data from a CSV and creates products via the Printify API.
    """
    print("🤖 Bulk Creator Agent: Initializing...")
    client = PrintifyApiClient()
    jobs_manager = FailedJobsManager("failed_creation_jobs.csv")
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            total = len(reader)
            print(f"Found {total} products to create.")

            for i, row in enumerate(reader):
                title = row.get('title', 'No Title')
                print(f"\n--- [{i+1}/{total}] Processing: '{title}' ---")
                
                try:
                    # --- 1. Parse variants and prices ---
                    variants_payload = []
                    variant_ids_for_print_area = []
                    for item in row['variants_and_prices'].split(','):
                        variant_id_str, price_str = item.split(':')
                        variant_id, price = int(variant_id_str), int(price_str)
                        variants_payload.append({"id": variant_id, "price": price, "is_enabled": True})
                        variant_ids_for_print_area.append(variant_id)

                    # --- 2. Construct the full API payload ---
                    product_payload = {
                        "title": title,
                        "description": row['description'],
                        "blueprint_id": int(row['blueprint_id']),
                        "print_provider_id": int(row['print_provider_id']),
                        "variants": variants_payload,
                        "print_areas": [{
                            "variant_ids": variant_ids_for_print_area,
                            "placeholders": [{
                                "position": "front",
                                "images": [{"id": row['image_id'], "x": 0.5, "y": 0.5, "scale": 1, "angle": 0}]
                            }]
                        }]
                    }
                    
                    # --- 3. Send the request ---
                    response = client.create_product(product_payload)
                    if response:
                        print(f"✅ Success! Product '{response['title']}' created.")
                    else:
                        raise Exception("API call failed, returned no response.")

                except Exception as e:
                    error_message = f"Failed to process product '{title}'. Reason: {e}"
                    print(f"❌ {error_message}")
                    jobs_manager.log_job(row, error_message)
                
                time.sleep(1) # Rate limit

    except FileNotFoundError:
        print(f"🚨 Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"🚨 An unexpected error occurred: {e}")

