from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, send_file
from user_database import UserDB
from subscriptions import SUBSCRIPTION_TIERS, has_access
from community import ProductReviews, Contests, Referrals
from nft_minting import mint_nft
from stripe_integration import create_checkout_session
from two_factor_auth import generate_otp_secret, generate_qr_code, verify_otp
from design_agent import generate_image_from_replicate, generate_ai_design
from civitai_client import CivitaiClient
from scheduler import start_scheduler
from legal_checker import check_for_trademarked_terms, check_for_patent_infringement, generate_legal_disclaimer
from robo_script_generator import generate_robo_script
from user_activity import UserActivity
from personalization import Personalization
from functools import wraps
from datetime import datetime
import os
import subprocess
from bi_agent import generate_bigquery_query, run_bigquery_query
from social_media_agent import SocialMediaAgent

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
social_media_agent = SocialMediaAgent()

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
    
@app.route("/api/design/generate-ai-design", methods=["POST"])
@login_required
@subscription_required('enterprise')
def api_generate_ai_design():
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "A prompt is required."}), 400

    image_result = generate_ai_design(prompt)

    if "error" in image_result:
        return jsonify(image_result), 500
    
    return jsonify(image_result)

@app.route("/bi-dashboard")
@login_required
@log_feature_use('bi_dashboard')
@subscription_required('business')
def bi_dashboard():
    return render_template("bi_dashboard.html")

@app.route("/bi-data")
@login_required
@subscription_required('business')
def bi_data():
    # In a real application, you would fetch this data from your database
    top_products = [
        {"product_name": "T-Shirt", "total_sales": 1500},
        {"product_name": "Mug", "total_sales": 1200},
        {"product_name": "Hoodie", "total_sales": 900},
        {"product_name": "Phone Case", "total_sales": 600},
        {"product_name": "Sticker", "total_sales": 300},
    ]
    sales_trends = [
        {"date": "2023-01-01", "total_sales": 500},
        {"date": "2023-01-02", "total_sales": 550},
        {"date": "2023-01-03", "total_sales": 620},
        {"date": "2023-01-04", "total_sales": 780},
        {"date": "2023-01-05", "total_sales": 710},
    ]
    sales_by_status = [
        {"status": "Completed", "count": 120},
        {"status": "Shipped", "count": 80},
        {"status": "In Production", "count": 50},
        {"status": "Cancelled", "count": 15},
    ]
    return jsonify({
        "top_products": top_products,
        "sales_trends": sales_trends,
        "sales_by_status": sales_by_status
    })

@app.route("/ask-bi", methods=["POST"])
@login_required
@subscription_required('business')
def ask_bi():
    natural_language_query = request.json.get("query")
    if not natural_language_query:
        return jsonify({"error": "A query is required."}), 400
    
    query_result = generate_bigquery_query(natural_language_query)
    
    if "error" in query_result:
        return jsonify(query_result), 500
        
    bigquery_query = query_result.get("query")
    if not bigquery_query:
        return jsonify({"error": "Could not generate a valid BigQuery query."}), 500
        
    results = run_bigquery_query(bigquery_query)
    
    if "error" in results:
        return jsonify(results), 500
        
    return jsonify({"results": results})
        
@app.route("/social-media-manager")
@login_required
@log_feature_use('social_media_manager')
@subscription_required('business')
def social_media_manager():
    return render_template("social_media_manager.html")

@app.route("/api/social-media/post", methods=["POST"])
@login_required
@subscription_required('business')
def api_social_media_post():
    product_name = request.json.get("product_name")
    product_description = request.json.get("product_description")
    image_url = request.json.get("image_url")

    if not all([product_name, product_description, image_url]):
        return jsonify({"error": "Product name, description, and image URL are required."}), 400

    result = social_media_agent.post_to_social_media(product_name, product_description, image_url)
    
    return jsonify(result)
    
@app.route("/marketing-dashboard")
@login_required
@log_feature_use('marketing_dashboard')
@subscription_required('business')
def marketing_dashboard():
    return render_template("marketing_dashboard.html")

@app.route("/api/marketing/generate-message", methods=["POST"])
@login_required
@subscription_required('business')
def api_marketing_generate_message():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Username is required."}), 400

    message = personalization_engine.generate_personalized_marketing_message(username)
    return jsonify({"message": message})

@app.route("/api/recommendations", methods=["POST"])
@login_required
def api_recommendations():
    username = request.json.get("username")
    if not username:
        return jsonify({"error": "Username is required."}), 400

    recommendations = personalization_engine.get_recommendations(username)
    return jsonify(recommendations)
    
@app.route("/legal-dashboard")
@login_required
@log_feature_use('legal_dashboard')
@subscription_required('business')
def legal_dashboard():
    return render_template("legal_dashboard.html")

@app.route("/api/legal/check", methods=["POST"])
@login_required
@subscription_required('business')
def api_legal_check():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text to check is required."}), 400

    trademark_result = check_for_trademarked_terms(text)
    patent_result = check_for_patent_infringement(text)
    
    return jsonify({
        "trademark": trademark_result,
        "patent": patent_result
    })

@app.route("/api/legal/generate-disclaimer", methods=["POST"])
@login_required
@subscription_required('business')
def api_legal_generate_disclaimer():
    product_type = request.json.get("product_type")
    if not product_type:
        return jsonify({"error": "Product type is required."}), 400

    disclaimer = generate_legal_disclaimer(product_type)
    return jsonify({"disclaimer": disclaimer})

# ... (rest of the routes)

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True, host='0.0.0.0', port=8080)
