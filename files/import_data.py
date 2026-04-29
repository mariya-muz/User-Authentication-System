import pandas as pd
from app import app
from db import db
from models import User
from security import encrypt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

df = pd.read_csv("users.csv")
df.columns = df.columns.str.strip()

with app.app_context():
   try:
      for _, row in df.iterrows():
        hashed = bcrypt.generate_password_hash(str(row["password"])).decode()

        user = User(
            name=row["name"],
            email_encrypted=encrypt(row["email"]),
            password_hash=hashed
        )
      print(row)
      db.session.add(user)
   except Exception as e:
      print("ERROR:", e)

      db.session.commit()


print("Dataset imported successfully")