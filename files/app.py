from flask import Flask, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import os

from db import db
from models import User
from security import encrypt, decrypt, generate_secret, verify_otp

from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db.init_app(app)
bcrypt = Bcrypt(app)

# OAuth setup
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "API is running"

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed = bcrypt.generate_password_hash(data["password"]).decode()

    user = User(
        name=data["name"],
        email_encrypted = encrypt(data["email"]),
        password_hash=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    users = User.query.all()
    matched_user = None

    for user in users:
        if decrypt(user.email_encrypted) == data["email"]:
            matched_user = user
            break

    if not matched_user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not bcrypt.check_password_hash(matched_user.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = matched_user.id

    if matched_user.is_2fa_enabled:
        return jsonify({"message": "2FA required"})

    return jsonify({"message": "Login successful"})

@app.route("/enable-2fa", methods=["POST"])
def enable_2fa():

    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    user = User.query.get(session["user_id"])

    secret = generate_secret()
    user.otp_secret = secret
    user.is_2fa_enabled = True

    db.session.commit()

    return jsonify({"secret": secret})

@app.route("/verify-2fa", methods=["POST"])
def verify_2fa():

    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    user = User.query.get(session["user_id"])
    code = request.json["code"]

    if verify_otp(user.otp_secret, code):
        session["2fa_verified"] = True
        return jsonify({"message": "2FA verified"})

    return jsonify({"error": "Invalid OTP"}), 400

@app.route("/login/google")
def google_login():
    return google.authorize_redirect(url_for("google_callback", _external=True))

@app.route("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()

    user_info = google.userinfo()

    email = user_info.get("email")
    name = user_info.get("name", "Google User")

    if not email:
        return jsonify({"error": "Google did not return email"}), 400

    users = User.query.all()
    user = None

    for u in users:
        try:
            if decrypt(u.email_encrypted) == email:
                user = u
                break
        except:
            continue

    if not user:
        user = User(
            name=name,
            email_encrypted=encrypt(email)
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id

    return jsonify({"message": "Google login successful"})

@app.route("/test-register")
def test_register():
    from models import User
    from db import db
    from flask_bcrypt import Bcrypt

    bcrypt = Bcrypt(app)

    hashed = bcrypt.generate_password_hash("123456").decode()

    user = User(
        name="test",
        email_encrypted=encrypt("test@gmail.com"),
        password_hash=hashed
    )
    

    db.session.add(user)
    db.session.commit()

    return "User created"

@app.route("/count")
def count_users():
    from models import User
    return str(User.query.count())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)