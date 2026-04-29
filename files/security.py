import os
from cryptography.fernet import Fernet
import pyotp
from dotenv import load_dotenv
load_dotenv()
# AES (via Fernet)
key = os.getenv("SECRET_KEY").encode()
cipher = Fernet(key)

def encrypt(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt(data):
    return cipher.decrypt(data.encode()).decode()

# OTP
def generate_secret():
    return pyotp.random_base32()

def verify_otp(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)