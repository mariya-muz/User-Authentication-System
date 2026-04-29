# Secure User Authentication System

## Overview
This project implements a secure authentication system using Flask with multiple layers of security including AES encryption, password hashing, Two-Factor Authentication (2FA), and OAuth 2.0 login via Google.

The system is designed to demonstrate modern authentication practices and secure handling of user data.

---

## Features

- User Registration and Login system
- Password hashing using bcrypt
- AES encryption for sensitive data (email)
- Two-Factor Authentication (Google Authenticator / TOTP)
- Google OAuth 2.0 login integration
- Session-based authentication
- Dataset import using Mockaroo-generated data

---

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Authlib (OAuth 2.0)
- PyOTP (2FA)
- Cryptography (AES encryption)
- Pandas (data import)

---

## Project Structure

auth-system/

│

├── app.py

├── db.py

├── models.py

├── security.py

├── import_data.py

├── users.csv

├── requirements.txt

├── README.md

└── screenshots/

---

## Setup Instructions

### 21. Create Virtual Environment

	python -m venv venv
	venv\Scripts\activate


### 3. Install Dependencies

	python -m pip install -r requirements.txt

### 4. Configure Environment Variables

Create a `.env` file:

	SECRET_KEY=your_secret_key
	DATABASE_URL=sqlite:///users.db
	GOOGLE_CLIENT_ID=your_google_client_id
	GOOGLE_CLIENT_SECRET=your_google_client_secret
	

### 5. Run Application

	python app.py
	
---

## Dataset Source

The dataset used in this project was generated using **Mockaroo** and imported into the system to simulate real user data for authentication testing.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /register | POST | Register a new user |
| /login | POST | Login user |
| /enable-2fa | POST | Enable 2FA |
| /verify-2fa | POST | Verify OTP |
| /login/google | GET | Google OAuth login |

---

## Security Implementation

### AES Encryption
  Sensitive user data (email) is encrypted before storage.

### Password Hashing
  Passwords are securely hashed using bcrypt.

### Two-Factor Authentication
  Time-based OTP generated using PyOTP and verified via Google Authenticator.

### OAuth 2.0
  Secure authentication via Google OAuth integration.

---

## Screenshots

### 1. Login Success

<img width="1919" height="1139" alt="1  login-success" src="https://github.com/user-attachments/assets/a73d490d-0a79-4796-83dc-10ee82f9a7a2" />


---

### 2. Google OAuth Setup (Google Cloud Console)

<img width="1870" height="1061" alt="2  oauth-cloud" src="https://github.com/user-attachments/assets/31b0fd19-2fe3-456c-8f1b-482398076095" />


---

### 3. Two-Factor Authentication Verified

<img width="1919" height="399" alt="3  2FA-verified" src="https://github.com/user-attachments/assets/14ae95c8-e8e8-41a5-aa09-d97b39b423b2" />


---

### 4. Mockaroo Dataset Generation

<img width="1855" height="1067" alt="4  mockaroo-data" src="https://github.com/user-attachments/assets/fcc9f8d1-f18c-46c0-8407-f1dd77614ce9" />


---

### 5. Final Project Structure

<img width="772" height="541" alt="5  file-structure" src="https://github.com/user-attachments/assets/b19fe46b-357a-4b5b-84e5-a3c54a090310" />


---

## Flow Summary

1. User registers → data encrypted + password hashed
2. User logs in → credentials validated
3. If 2FA enabled → OTP required
4. OTP verified → session created
5. Optional login via Google OAuth

---

## Conclusion

This project demonstrates a secure, multi-layered authentication system incorporating modern security standards including encryption, multi-factor authentication, and OAuth 2.0 integration.
