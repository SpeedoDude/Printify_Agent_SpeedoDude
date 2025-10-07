# two_factor_auth.py

import pyotp
import qrcode
import io

def generate_otp_secret():
    """Generates a new OTP secret."""
    return pyotp.random_base32()

def generate_qr_code(secret, username, issuer_name="Printify Manager"):
    """Generates a QR code for the OTP secret."""
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer_name)
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf

def verify_otp(secret, otp):
    """Verifies an OTP code."""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)
