from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask("JetCert Example")

import main.db

import main.modules

import main.middlewares

import main.handlers
