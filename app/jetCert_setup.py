# Setup JetCert
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
