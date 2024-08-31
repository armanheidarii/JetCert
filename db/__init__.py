# Basic Packages
import os
import sys

# App Packages
from flask_sqlalchemy import SQLAlchemy
from app import app


# Database Setup
db_path = os.getenv("DB_URI")
db_path_parent = os.path.dirname(db_path)
os.makedirs(db_path_parent, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

public_id_len = 50
name_len = 100
email_len = 70
password_len = 80


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(public_id_len), unique=True)
    name = db.Column(db.String(name_len))
    email = db.Column(db.String(email_len), unique=True)
    password = db.Column(db.String(password_len))


with app.app_context():
    db.create_all()
