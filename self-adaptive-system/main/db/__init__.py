# Basic Packages
import os
import sys

# App Packages
from flask_sqlalchemy import SQLAlchemy
from main import app


db_path = os.getenv("DB_URI")
db_path_parent = os.path.dirname(db_path)
os.makedirs(db_path_parent, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from main.db.models import user

with app.app_context():
    db.create_all()
