from main.db import db

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
