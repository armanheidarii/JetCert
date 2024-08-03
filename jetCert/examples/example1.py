import sys

sys.path.append(".")

from jetCert import JetCert

jet_cert = JetCert.create(modules_path="modules", period=2)

Login = jet_cert.add_module(
    "login",
    python_entry_file_name="__main__",
    fast_compilation_tool="python",
    c_entry_file_name="main",
    c_linked_files=["sqlite3"],
    wait_to_ready=True,
)

jet_cert.start()

print(jet_cert.get_module("login"))
print(jet_cert.get_all_modules())

response = Login.run(inputs={"email": "arman", "password": "arman"})
print(f"\nFinal Res\n{response}")
