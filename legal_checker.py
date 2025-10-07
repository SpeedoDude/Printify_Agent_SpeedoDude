# legal_checker.py

from logic import get_gemini_vision_pro_model
from PIL import Image, ImageDraw, ImageFont
import io

# In a real application, you would use a comprehensive legal database.
TRADEMARK_DATABASE = {"disney", "nike", "coca-cola", "marvel", "star wars"}
PATENT_DATABASE = {"selfie stick", "pop socket", "fidget spinner"} # Simplified for demonstration

def check_for_trademarked_terms(text):
    """
    Checks for trademarked terms in a string of text against a simulated database.
    """
    found_terms = {term for term in TRADEMARK_DATABASE if term in text.lower()}
    
    if found_terms:
        return {"status": "failed", "message": f"Found potential trademarked terms: {', '.join(found_terms)}."}
    return {"status": "success", "message": "No trademarked terms found."}

def check_for_patent_infringement(text):
    """
    Checks for potential patent infringement in a product description.
    """
    found_patents = {patent for patent in PATENT_DATABASE if patent in text.lower()}
    
    if found_patents:
        return {"status": "failed", "message": f"Product description may infringe on patents for: {', '.join(found_patents)}."}
    return {"status": "success", "message": "No potential patent infringements found."}

def generate_legal_disclaimer(product_type):
    """
    Generates a generic legal disclaimer for a product page using an AI model.
    """
    try:
        model = get_gemini_vision_pro_model()
        prompt = f"""
        Generate a concise legal disclaimer for a product page.
        The product is a "{product_type}".
        The disclaimer should cover topics like intellectual property, liability, and terms of use.
        It should be easy for a layperson to understand.

        Return the response as a JSON object with a "disclaimer" key.
        """
        response = model.generate_content([prompt])
        
        import json
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        disclaimer_data = json.loads(clean_response)
        
        return disclaimer_data.get("disclaimer")
    except Exception as e:
        print(f"An error occurred while generating legal disclaimer: {e}")
        return "Disclaimer: All designs are user-submitted. We are not liable for any copyright or trademark infringement."

def analyze_image_for_copyright(image_path):
    """
    Analyzes an image for copyrighted content using an AI model.
    """
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
            # You might need to adjust the font path
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except IOError:
                font = ImageFont.load_default()
            draw.text((10, 10), text, font=font, fill=(255, 255, 255, 128))
            
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return buf
    except Exception as e:
        print(f"An error occurred while adding watermark: {e}")
        return None
