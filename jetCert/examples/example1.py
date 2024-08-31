import sys

sys.path.append(".")

from jetCert import JetCert

jet_cert = JetCert.create(modules_path="modules", period=2)

Login = jet_cert.add_module(
    "login",
    python_entry_file_name="__main__",
    fast_compilation_tool="python",
    c_entry_file_name="main",
    c_linked_files=["json-c", "sqlite3"],
)

jet_cert.start()

Crypto = jet_cert.add_module(
    "cryptography",
    python_entry_file_name="__main__",
    fast_compilation_tool="python",
    c_entry_file_name="main",
    c_linked_files=["json-c", "m"],
    wait_to_ready=True,
)

print(jet_cert.get_module("login"))
print(jet_cert.get_module("cryptography"))
print(jet_cert.get_all_modules())

login_response = Login.run(inputs={"email": "hi", "password": "bye"})
print(f"\nFinal Login Res\n{login_response}")

crypto_response = Crypto.run(inputs={"plaintext": "armanheids@gmail.com"})
print(f"\nFinal Crypto Res\n{crypto_response}")
