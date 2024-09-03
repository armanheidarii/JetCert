from dotenv import load_dotenv
from flask import Flask

# Load .env
load_dotenv()

# Setup app
app = Flask("JetCert Example")

# Setup Database
import main.db

# Setup JetCert Modules
import main.modules

# Setup Middlewares
from main.middlewares import login

# Setup Handlers
from main.handlers import (
    signup,
    black_scholes,
    lennard_jones,
    get_all_users,
    delete_user,
)
