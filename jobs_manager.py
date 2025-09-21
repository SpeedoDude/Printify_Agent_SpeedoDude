# jobs_manager.py

import csv
import os
import json

class FailedJobsManager:
    def __init__(self, file_path="failed_creation_jobs.csv"):
        self.file_path = file_path
        # Define headers for the CSV file
        self.fieldnames = [
            'title', 'description', 'blueprint_id', 'print_provider_id',
            'variants', 'print_areas', 'error'
        ]

    def log_job(self, payload, error_message):
        """Logs a failed product creation payload to the CSV."""
        # Make a copy to avoid modifying the original dict
        data_row = payload.copy()
        data_row['error'] = str(error_message)

        # Convert complex objects to JSON strings for CSV compatibility
        data_row['variants'] = json.dumps(data_row.get('variants', []))
        data_row['print_areas'] = json.dumps(data_row.get('print_areas', []))

        file_exists = os.path.isfile(self.file_path)
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                if not file_exists:
                    writer.writeheader()
                
                # Write only the fields defined in fieldnames
                writer.writerow({k: v for k, v in data_row.items() if k in self.fieldnames})
        except Exception as e:
            print(f"CRITICAL: Could not write to failed jobs log. Reason: {e}")

    def get_jobs(self):
        """Reads all failed jobs from the CSV."""
        if not os.path.isfile(self.file_path):
            return []
        
        with open(self.file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    def clear_log(self):
        """Deletes the log file."""
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

