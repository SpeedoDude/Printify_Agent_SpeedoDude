# error_handlers.py

from flask import render_template
from printify_client import PrintifyClient

def handle_500(e):
    """Handles 500 Internal Server Errors."""
    return render_template("error.html", error=e), 500

def handle_404(e):
    """Handles 404 Not Found Errors."""
    return render_template("404.html"), 404
    
def auto_fix_publish_error(shop_id, product_id):
    """
    Attempts to automatically fix a product publishing error.
    """
    client = PrintifyClient()
    
    # 1. Unpublish the product
    unpublish_result = client.unpublish_product(shop_id, product_id)
    if not unpublish_result:
        return {"success": False, "message": "Failed to unpublish the product."}
        
    # 2. Re-publish the product
    publish_result = client.publish_product(shop_id, product_id)
    if not publish_result:
        return {"success": False, "message": "Failed to re-publish the product."}
        
    # 3. Verify the publication status
    status = client.get_publication_status(shop_id, product_id)
    if status == "published":
        return {"success": True, "message": "Successfully fixed the publishing error."}
    else:
        return {"success": False, "message": "Failed to verify the publication status."}
