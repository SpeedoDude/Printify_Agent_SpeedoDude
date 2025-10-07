from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, send_file
from user_database import UserDB
from subscriptions import SUBSCRIPTION_TIERS, has_access
from community import ProductReviews, Contests, Referrals
from nft_minting import mint_nft
from stripe_integration import create_checkout_session
from two_factor_auth import generate_otp_secret, generate_qr_code, verify_otp
from design_agent import generate_image_from_replicate
from civitai_client import CivitaiClient
from scheduler import start_scheduler
from legal_checker import check_for_trademarked_terms, analyze_image_for_copyright, add_watermark
from robo_script_generator import generate_robo_script
from user_activity import UserActivity
from personalization import Personalization
from functools import wraps
from datetime import datetime
import os
import subprocess

# ... (imports from previous step)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Change this!
app.config['UPLOAD_FOLDER'] = 'uploads'

# ... (error handlers, file uploads, printify client)

user_db = UserDB()
reviews_db = ProductReviews()
contests_db = Contests()
referrals_db = Referrals()
activity_db = UserActivity()
personalization_engine = Personalization()
civitai_client = CivitaiClient()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def subscription_required(feature):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = user_db.get_user(session['username'])
            if not has_access(user.subscription_tier, feature):
                flash(f"You need to upgrade your subscription to access this feature.", "warning")
                return redirect(url_for('upgrade'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
    
def log_feature_use(feature):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            activity_db.log_activity(session['username'], 'use_feature', {'feature': feature})
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = user_db.authenticate_user(username, password)
        if user:
            session['username'] = user.username
            activity_db.log_activity(username, 'login')
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
        return redirect(url_for('login'))
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route("/")
@login_required
@log_feature_use('dashboard')
def dashboard():
    recommendations = personalization_engine.get_recommendations(session['username'])
    # ... (existing dashboard logic)
    return render_template("dashboard.html", recommendations=recommendations, failed_jobs=len(failed_jobs))
    
@app.route("/design-studio")
@login_required
@log_feature_use('design_studio')
def design_studio():
    return render_template("design_studio.html")

@app.route("/api/civitai/search", methods=["POST"])
@login_required
@subscription_required('enterprise')
def api_civitai_search():
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "A search query is required."}), 400
    
    models = civitai_client.search_models(query)
    return jsonify(models)

@app.route("/api/design/generate-image", methods=["POST"])
@login_required
@subscription_required('enterprise')
def api_generate_image():
    model_version = request.json.get("model_version")
    prompt = request.json.get("prompt")
    lora = request.json.get("lora")

    if not all([model_version, prompt]):
        return jsonify({"error": "Model version and prompt are required."}), 400

    image_result = generate_image_from_replicate(model_version, prompt, lora)

    if "error" in image_result:
        return jsonify(image_result), 500
    
    return jsonify(image_result)

# ... (rest of the routes)

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True, host='0.0.0.0', port=8080)
