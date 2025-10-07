from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, send_file
from user_database import UserDB
from subscriptions import SUBSCRIPTION_TIERS, has_access
from design_agent import generate_image_from_replicate, generate_ai_design
from civitai_client import CivitaiClient
from legal_checker import check_for_trademarked_terms, check_for_patent_infringement, generate_legal_disclaimer
from social_media_agent import SocialMediaAgent
from seo_agent import SEOAgent
from legal_tech import LegalTechAgent
from jobs_manager import jobs_manager
from functools import wraps
import threading
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Change this!
app.config['UPLOAD_FOLDER'] = 'uploads'

user_db = UserDB()
civitai_client = CivitaiClient()
social_media_agent = SocialMediaAgent()
seo_agent = SEOAgent()
legal_tech_agent = LegalTechAgent()

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

def run_background_job(job_id, target, args):
    try:
        result = target(*args)
        jobs_manager.update_job_status(job_id, 'completed', result)
    except Exception as e:
        jobs_manager.update_job_status(job_id, 'failed', str(e))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = user_db.authenticate_user(username, password)
        if user:
            session['username'] = user.username
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
def dashboard():
    failed_jobs = jobs_manager.get_failed_jobs()
    return render_template("dashboard.html", recommendations=[], failed_jobs=len(failed_jobs))

@app.route("/design-studio")
@login_required
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

@app.route("/social-media-manager")
@login_required
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

@app.route("/legal-dashboard")
@login_required
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

@app.route('/run-legal-tech', methods=['POST'])
@login_required
def run_legal_tech():
    legal_tech_task = request.form.get('legal_tech_task')
    target_map = {
        'contract_generation': legal_tech_agent.generate_contract,
        'ediscovery': legal_tech_agent.run_ediscovery,
        'legal_research': legal_tech_agent.conduct_legal_research,
    }
    target = target_map.get(legal_tech_task)
    if target:
        job_id = jobs_manager.add_job(target, [])
        threading.Thread(target=run_background_job, args=(job_id, target, [])).start()
        flash(f'Legal tech task "{legal_tech_task}" has been started in the background.', 'success')
    else:
        flash('Invalid legal tech task selected.', 'danger')
    return redirect(url_for('dashboard'))

@app.route("/seo-optimizer")
@login_required
def seo_optimizer():
    return render_template("seo_optimizer.html")

@app.route("/api/seo/analyze", methods=["POST"])
@login_required
def analyze_seo():
    return jsonify({"message": "SEO analysis is not implemented yet."})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)