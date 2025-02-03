import os
import time
import traceback
import threading
import csv

from builder import Builder


class MAPE:
    def __init__(self, system, period=60):
        if not system:
            raise ValueError(f"The system {system} cannot be empty!")
        self.system = system

        if period <= 0:
            raise ValueError(f"The period {period} is not positive!")
        self.period = period

        self.MAPE_folder_name = "__mape__"

        modules_path = self.system.get_modules_path()
        MAPE_folder_path = os.path.join(modules_path, self.MAPE_folder_name)
        if not os.path.exists(MAPE_folder_path):
            raise ValueError(f"The MAPE_folder_path {MAPE_folder_path} does not exist!")
        self.MAPE_folder_path = MAPE_folder_path

        monitor_path = os.path.join(self.MAPE_folder_path, "monitor")
        if not os.path.exists(monitor_path):
            raise ValueError(f"The monitor_path {monitor_path} does not exist!")
        self.monitor_path = monitor_path

        analyse_path = os.path.join(self.MAPE_folder_path, "analyse")
        if not os.path.exists(analyse_path):
            raise ValueError(f"The analyse_path {analyse_path} does not exist!")
        self.analyse_path = analyse_path

        plan_path = os.path.join(self.MAPE_folder_path, "plan")
        if not os.path.exists(plan_path):
            raise ValueError(f"The plan_path {plan_path} does not exist!")
        self.plan_path = plan_path

        self.is_start_flag = False
        self.is_start_event = threading.Event()
        self.itr = 0

        cache_folder_path = self.system.get_cache_folder_path()
        self.data_file_name = "mape.csv"
        self.data_file_path = os.path.join(cache_folder_path, self.data_file_name)
        self.data_columns = [
            "Monitor Time",
            "Analyse Time",
            "Plan Time",
            "Execute Time",
        ]
        self.data_write(self.data_columns, mode="w")

    def get_period(self):
        return self.period

    def get_MAPE_folder_name(self):
        return self.MAPE_folder_name

    def get_MAPE_folder_path(self):
        return self.MAPE_folder_path

    def get_monitor_path(self):
        return self.monitor_path

    def get_analyse_path(self):
        return self.analyse_path

    def get_plan_path(self):
        return self.plan_path

    def get_execute_path(self):
        return self.execute_path

    def is_start(self):
        return self.is_start_flag

    def get_itr(self):
        return self.itr

    def get_MAPE_model(self):
        return self.MAPE_model

    def data_write(self, data, mode="w"):
        f = open(self.data_file_path, mode=mode, newline="", encoding="utf-8")
        data_writer = csv.writer(f)
        data_writer.writerow(data)

    def start(self):
        threading.Thread(target=self.MAPE).start()
        self.is_start_event.wait()

        self.is_start_flag = True

    def monitor(self):
        start = time.time()
        response = Builder.run_python_file(self.monitor_path)
        end = time.time()
        if self.system.is_continuous_deployment_active():
            self.system.update_CD()

        return response.get("result"), end - start

    def analyse(self, monitor_data):
        start = time.time()
        response = Builder.run_python_file(self.analyse_path, inputs=monitor_data)
        end = time.time()

        return response.get("result"), end - start

    def plan(self, analyse_data):
        start = time.time()
        response = Builder.run_python_file(self.plan_path, inputs=analyse_data)
        end = time.time()

        return response.get("result"), end - start

    def execute(self, plan_data):
        if not plan_data:
            raise ValueError(f"The plan_data {plan_data} cannot be empty!")

        for module_name, data in plan_data.items():
            module = self.system.get_module(module_name)
            if module:
                module.execute(data)

    def update(self):
        start = time.time()
        monitor, monitor_time = self.monitor()
        analyse, analyse_time = self.analyse(monitor)
        plan, plan_time = self.plan(analyse)
        execute_time = self.period - monitor_time - analyse_time - plan_time
        self.execute(plan)

        self.data_write([monitor_time, analyse_time, plan_time, execute_time], mode="a")

        self.itr += 1
        end = time.time()

        return end - start

    def MAPE(self):
        last_MAPEs_delay = 0

        print(f"start MAPE round 0")
        try:
            updates_time = self.update()

        except:
            raise ValueError(f"The MAPE is not setup correctly!")

        self.is_start_event.set()

        while True:
            try:
                MAPE_delay = max(
                    0,
                    self.itr * self.period - last_MAPEs_delay - updates_time,
                )
                time.sleep(MAPE_delay)
                last_MAPEs_delay += MAPE_delay
                print(f"finish MAPE round {self.itr - 1}")

                print(f"start MAPE round {self.itr}")
                updates_time += self.update()

            except:
                traceback.print_exc()

    def __str__(self):
        MAPE_status = "start" if self.is_start_flag else "not start"
        return f"<MAPE ({MAPE_status}) in {self.period}>"
