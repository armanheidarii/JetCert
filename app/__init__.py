from dotenv import load_dotenv
from flask import Flask
from jetCert import JetCert


# Load .env
load_dotenv()


# Setup app
app = Flask("JetCert Example")


# Setup JetCert
jet_cert = JetCert.create(modules_path="modules", period=2)

Login = jet_cert.add_module(
    "login",
    fast_compilation_tool="python",
    fast_entry_file_name="__main__",
    safe_entry_file_name="main",
    safe_linked_files=["json-c", "sqlite3"],
)

Crypto = jet_cert.add_module(
    "cryptography",
    safe_entry_file_name="main",
    safe_linked_files=["json-c", "m"],
)

Finance = jet_cert.add_module(
    "finance",
    fast_compilation_tool="numba",
    fast_entry_file_name="__main__",
    fast_numba_entry_func_name="go_fast",
)

Physics = jet_cert.add_module(
    "physics",
    fast_compilation_tool="numba",
    fast_entry_file_name="__main__",
    fast_numba_entry_func_name="go_fast",
)

jet_cert.start()


# Setup Handlers
from app.handlers import (
    signup,
    black_scholes,
    lennard_jones,
    get_all_users,
    delete_user,
)
