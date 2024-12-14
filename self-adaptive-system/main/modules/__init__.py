import os
import sys

sys.path.append(".")
# change: use from pip
from JetCert import JetCert

jetcert = JetCert(
    period=4,
    modules_path=os.getenv("MODULES_PATH"),
    config_files_name="config.toml",
    continuous_deployment=True,
)
jetcert.start()

Login = jetcert.get_module("login")
Crypto = jetcert.get_module("cryptography")
Finance = jetcert.get_module("finance")
Physics = jetcert.get_module("physics")
