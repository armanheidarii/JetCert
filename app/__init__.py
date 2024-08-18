from flask import Flask

# Setup app
app = Flask("JetCert Example")


# Setup JetCert
from jetCert import JetCert

jet_cert = JetCert.create(modules_path="modules", period=2)

Login = jet_cert.add_module(
    "login",
    python_entry_file_name="__main__",
    fast_compilation_tool="python",
    c_entry_file_name="main",
    c_linked_files=["sqlite3", "json-c"],
)

Crypto = jet_cert.add_module(
    "cryptography",
    python_entry_file_name="__main__",
    fast_compilation_tool="python",
    c_entry_file_name="main",
    c_linked_files=["json-c", "m"],
)

jet_cert.start()


# Setup Handlers
from app.handlers import signup, get_all_users
