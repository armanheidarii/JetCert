import os
import sys
from dotenv import load_dotenv

sys.path.append(".")
# change: use from pip
from jetCert import JetCert

load_dotenv()

jet_cert = JetCert.create(
    period=2,
    modules_path=os.getenv("MODULES_PATH"),
    capture_MAPE_data=True,
    MAPE_data_path=os.getenv("MAPE_DATA_PATH"),
)

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

MAPE_data = jet_cert.get_MAPE_data(limit=10, offset=2, wait_to_ready=True)

iterations_count = MAPE_data.get("iterations_count")
monitor_execution_times = MAPE_data.get("monitor_execution_times")
analyse_execution_times = MAPE_data.get("analyse_execution_times")
planning_execution_times = MAPE_data.get("planning_execution_times")
execute_execution_times = MAPE_data.get("execute_execution_times")
overall_execution_times = MAPE_data.get("overall_execution_times")
safe_intervals = MAPE_data.get("safe_intervals")

x = list(range(0, iterations_count))

import MAPE_plt
import interval_plt

MAPE_plt.show(
    x,
    monitor_execution_times,
    analyse_execution_times,
    planning_execution_times,
    execute_execution_times,
)

interval_plt.show(x, overall_execution_times, safe_intervals)
