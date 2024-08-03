import sys

sys.path.append(".")

import os
from flask_sqlalchemy import SQLAlchemy
from app import app

basedir = os.path.abspath(os.path.dirname(__file__))

directory = "instance"
db_base = os.path.join(basedir, directory)

if not os.path.exists(db_base):
    os.mkdir(db_base)

db_name = "Database.db"
db_path = os.path.join(db_base, db_name)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# creates SQLALCHEMY object
db = SQLAlchemy(app)

# Migrate User
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
