# nft_minting.py

import random
import string
import time

def mint_nft(product_id, owner_address):
    """
    Mints an NFT for a product.
    In a real application, this would involve interacting with a blockchain.
    """
    # Simulate the minting process
    time.sleep(2)
    
    # Generate a mock transaction hash
    transaction_hash = ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
    
    return {
        "success": True,
        "message": f"Successfully minted NFT for product {product_id}",
        "transaction_hash": transaction_hash,
        "owner_address": owner_address
    }
