# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Import agent functions we want to trigger
from bulk_updater import update_products_from_csv

# --- Flask App Configuration ---
app = Flask(__name__)
app.secret_key = "supersecretkey" # Required for flash messages
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Routes ---

@app.route('/')
def index():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/run-bulk-update', methods=['POST'])
def run_bulk_update_route():
    """Handles file upload and triggers the bulk update agent."""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and file.filename.endswith('.csv'):
        # Save the uploaded file securely
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # --- Call the existing agent logic ---
            # We pass the path of the newly uploaded file to the agent function.
            # For a more advanced implementation, we would capture the logs here.
            update_products_from_csv(file_path)
            flash(f'Bulk update process started successfully with file: {filename}', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'error')

        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a .csv file.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
