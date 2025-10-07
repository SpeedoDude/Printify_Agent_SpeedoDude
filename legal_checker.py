# legal_checker.py

from logic import get_gemini_vision_pro_model
from PIL import Image, ImageDraw, ImageFont
import io

def check_for_trademarked_terms(text):
    """
    Checks for trademarked terms in a string of text.
    In a real application, this would involve checking against a database of trademarked terms.
    """
    # Simulate a trademark check
    trademarked_terms = ["disney", "nike", "coca-cola"]
    found_terms = []
    for term in trademarked_terms:
        if term in text.lower():
            found_terms.append(term)
    
    if found_terms:
        return {"status": "failed", "message": f"Found trademarked terms: {', '.join(found_terms)}"}
    return {"status": "success", "message": "No trademarked terms found."}

def analyze_image_for_copyright(image_path):
    """
    Analyzes an image for copyrighted content using an AI model.
    """
    # AI Prompt tailored for copyright analysis
    prompt = """
    Analyze the following image for any copyrighted content, such as logos, characters, or artwork.
    If you find any copyrighted content, please identify it and explain why it may be copyrighted.
    If you do not find any copyrighted content, please confirm that the image appears to be free of copyright issues.
    """

    try:
        model = get_gemini_vision_pro_model()
        response = model.generate_content([prompt, {"path": image_path}])
        
        return {"status": "success", "message": response.text}

    except Exception as e:
        print(f"An error occurred while analyzing image for copyright: {e}")
        return {"status": "failed", "message": f"Failed to analyze image for copyright. Raw response: {str(e)}"}

def add_watermark(image_path, text="Copyright Printify Manager"):
    """
    Adds a watermark to an image.
    """
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 36)
            draw.text((10, 10), text, font=font, fill=(255, 255, 255, 128))
            
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return buf
    except Exception as e:
        print(f"An error occurred while adding watermark: {e}")
        return None
