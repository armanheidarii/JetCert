import os
import sys
from dotenv import load_dotenv

sys.path.append(".")
# change: use from pip
from JetCert import JetCert


load_dotenv()

jetcert = JetCert(
    period=2,
    modules_path=os.getenv("MODULES_PATH"),
    config_files_name="config.toml",
    continuous_deployment=True,
)
jetcert.start()

Login = jetcert.get_module("login")
Crypto = jetcert.get_module("cryptography")
Finance = jetcert.get_module("finance")
Physics = jetcert.get_module("physics")

MAPE_data = jetcert.get_MAPE_data(limit=25, offset=2, wait_to_ready=True)

x = list(range(0, len(MAPE_data)))
monitor_execution_times = [item.monitor_execution_time for item in MAPE_data]
analyse_execution_times = [item.analyse_execution_time for item in MAPE_data]
plan_execution_times = [item.plan_execution_time for item in MAPE_data]
execute_execution_times = [item.execute_execution_time for item in MAPE_data]
overall_execution_times = [item.overall_execution_time for item in MAPE_data]

import specific_mape_plt
import overall_mape_plt

specific_mape_plt.show(
    x,
    monitor_execution_times,
    analyse_execution_times,
    plan_execution_times,
    execute_execution_times,
)

overall_mape_plt.show(x, overall_execution_times)
