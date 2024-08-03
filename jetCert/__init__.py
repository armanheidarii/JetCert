import os
import subprocess
import traceback
import time
import threading
import json


class Builder:
    fast_compilation_tools = ["numba", "codon", "python"]

    def __init__(self, module):
        self.module = module

    def create(module):
        return Builder(module)

    def is_json(input_string):
        try:
            json.loads(input_string)
            return True
        except json.JSONDecodeError:
            return False

    def run_cmd(cmd, inputs=None):
        if inputs != None:
            inputs = f"{json.dumps(inputs)}"

        completed_process = subprocess.run(
            cmd, input=inputs, capture_output=True, text=True
        )

        return {
            "returncode": completed_process.returncode,
            "stdout": completed_process.stdout,
            "stderr": completed_process.stderr,
            "args": " ".join(completed_process.args),
        }

    def run_exe_file(file_path, inputs=None):
        response = Builder.run_cmd([file_path], inputs=inputs)

        stdout = response.get("stdout")
        return {
            "process": response,
            "result": (json.loads(stdout) if Builder.is_json(stdout) else stdout),
        }

    def run_python_file(file_path, inputs=None):
        response = Builder.run_cmd(["python", file_path], inputs=inputs)

        stdout = response.get("stdout")
        return {
            "process": response,
            "result": (json.loads(stdout) if Builder.is_json(stdout) else stdout),
        }

    def run_numba_file(file_path, inputs=None):
        response = Builder.run_cmd(["numba", file_path], inputs=inputs)

        stdout = response.get("stdout")
        return {
            "process": response,
            "result": (json.loads(stdout) if Builder.is_json(stdout) else stdout),
        }

    def compile_safe_versions(self):
        file_paths = self.module.get_state_files_path("safe")
        for file_path in file_paths:

            base_cmd = ["gcc", "tools/cJSON/cJSON.c", f"{file_path}.c"]
            linked_cmd = [
                f"-l{linked_file}" for linked_file in self.module.c_linked_files
            ]
            output_cmd = ["-o", file_path]
            cmd = base_cmd + linked_cmd + output_cmd
            response = Builder.run_cmd(cmd)

            print(response)

    def compile_fast_versions(self):
        file_paths = self.module.get_state_files_path("fast")
        for file_path in file_paths:
            base_cmd = ["codon", "build", "-release", "-exe", f"{file_path}.py"]
            response = Builder.run_cmd(base_cmd)

            print(response)


class Module:
    def __init__(
        self,
        system,
        module_name,
        python_entry_file_name="__main__",
        fast_compilation_tool="python",
        c_entry_file_name="main",
        c_linked_files=[],
    ):
        self.system = system
        self.module_name = module_name
        self.python_entry_file_name = python_entry_file_name
        self.fast_compilation_tool = fast_compilation_tool
        self.c_entry_file_name = c_entry_file_name
        self.c_linked_files = c_linked_files
        self.is_ready_flag = True
        self.is_active_flag = True
        self.safety = {"state": "safe", "level": 1}
        self.builder = Builder.create(self)
        self.module_lock = threading.Lock()

    def create(
        system,
        module_name,
        python_entry_file_name="__main__",
        fast_compilation_tool="python",
        c_entry_file_name="main",
        c_linked_files=[],
    ):

        if not fast_compilation_tool in Builder.fast_compilation_tools:
            return None

        module = Module(
            system,
            module_name,
            python_entry_file_name=python_entry_file_name,
            fast_compilation_tool=fast_compilation_tool,
            c_entry_file_name=c_entry_file_name,
            c_linked_files=c_linked_files,
        )

        module.builder.compile_safe_versions()

        if module.fast_compilation_tool == "codon":
            module.builder.compile_fast_versions()

        return module

    def is_ready(self):
        try:
            return self.is_ready_flag

        except:
            traceback.print_exc()
            return None

    def active(self):
        try:
            self.is_active_flag = True

        except:
            traceback.print_exc()
            return None

    def inactive(self):
        try:
            self.is_active_flag = False

        except:
            traceback.print_exc()
            return None

    def is_active(self):
        try:
            return self.is_active_flag

        except:
            traceback.print_exc()
            return None

    def get_status(self):
        return (
            ("active" if self.is_active_flag else "inactive")
            if self.is_ready_flag
            else "pending"
        )

    def get_safety(self):
        return self.safety.copy()

    def run(self, inputs=None):
        try:
            if not self.is_ready() or not self.is_active():
                return None

            safety = self.safety.copy()
            file_path = self.get_file_path(safety.get("state"), safety.get("level"))

            response = None
            if safety.get("state") == "fast":

                if self.fast_compilation_tool == "numba":
                    response = Builder.run_numba_file(
                        f"{file_path}.py", inputs=inputs
                    ).copy()

                if self.fast_compilation_tool == "codon":
                    response = Builder.run_exe_file(file_path, inputs=inputs).copy()

                if self.fast_compilation_tool == "python":
                    response = Builder.run_python_file(
                        f"{file_path}.py", inputs=inputs
                    ).copy()

            elif safety.get("state") == "safe":
                response = Builder.run_exe_file(file_path, inputs=inputs).copy()

            response["safety"] = safety

            return response

        except:
            traceback.print_exc()
            return None

    def monitor(self):
        try:
            monitor_file_path = self.get_mape_file_path("monitor")
            response = Builder.run_python_file(monitor_file_path)
            return response.get("result")

        except:
            traceback.print_exc()
            return None

    def analyse(self, monitor_data):
        try:
            analyse_file_path = self.get_mape_file_path("analyse")
            response = Builder.run_python_file(analyse_file_path, inputs=monitor_data)
            return response.get("result")

        except:
            traceback.print_exc()
            return None

    def planning(self, analyse_data):
        try:
            planning_file_path = self.get_mape_file_path("planning")
            response = Builder.run_python_file(planning_file_path, inputs=analyse_data)
            return response.get("result")

        except:
            traceback.print_exc()
            return None

    def execute(self, planning_data):
        try:
            self.module_lock.acquire()
            self.safety = planning_data
            self.module_lock.release()

        except:
            traceback.print_exc()

    def get_module_path(self):
        return f"{self.system.modules_path}/{self.module_name}"

    def get_state_path(self, safety_state):
        module_path = self.get_module_path()
        return f"{module_path}/{safety_state}"

    def get_level_path(self, safety_state, safety_level):
        state_path = self.get_state_path(safety_state)
        return f"{state_path}/level{safety_level}"

    def get_file_path(self, safety_state, safety_level):
        level_path = self.get_level_path(safety_state, safety_level)
        entry_file_name = (
            self.python_entry_file_name
            if safety_state == "fast"
            else self.c_entry_file_name
        )
        return f"{level_path}/{entry_file_name}"

    def get_state_files_path(self, safety_state):
        state_path = self.get_state_path(safety_state)
        state_levels_path = []
        for name in os.listdir(state_path):
            if name.startswith("level"):
                file_path = self.get_file_path(
                    safety_state, int(name[name.rfind("l") + 1 :])
                )
                state_levels_path.append(f"{file_path}")
        return state_levels_path

    def get_mape_file_path(self, file_name):
        module_path = self.get_module_path()
        return f"{module_path}/MAPE/{file_name}.py"

    def __str__(self):
        safety = self.safety.copy()
        safety_state = safety.get("state")
        safety_level = safety.get("level")

        return f"<Module {self.module_name} ({self.get_status()}) in state {safety_state} and level {safety_level}>"


class JetCert:
    def __init__(self, modules_path=".", period=60):
        self.modules_path = modules_path
        self.MAPE = MAPE.create(self, period)
        self.modules = dict()
        self.pending_modules = list()
        self.lock = threading.Lock()

    def create(modules_path=".", period=60):
        try:
            if period <= 0:
                return None

            return JetCert(modules_path=modules_path, period=period)

        except:
            traceback.print_exc()
            return None

    def start(self):
        try:
            self.MAPE.start()
            return True

        except:
            traceback.print_exc()
            return False

    def is_start(self):
        try:
            return self.MAPE.is_start()

        except:
            traceback.print_exc()
            return None

    def stop(self):
        try:
            self.MAPE.stop()
            return True

        except:
            traceback.print_exc()
            return False

    def is_stop(self):
        try:
            return self.MAPE.is_stop()

        except:
            traceback.print_exc()
            return None

    def add_module(
        self,
        module_name,
        python_entry_file_name="__main__",
        fast_compilation_tool="python",
        c_entry_file_name="main",
        c_linked_files=[],
        wait_to_ready=False,
    ):
        try:
            self.lock.acquire()

            if not fast_compilation_tool in Builder.fast_compilation_tools:
                return None

            module = self.get_module(module_name)
            if module != None:
                return module

            module = Module.create(
                self,
                module_name,
                python_entry_file_name=python_entry_file_name,
                fast_compilation_tool=fast_compilation_tool,
                c_entry_file_name=c_entry_file_name,
                c_linked_files=c_linked_files,
            )

            self.modules[module_name] = module

            if self.is_start():
                self.pending_modules.append(module_name)
                module.is_ready_flag = False

            self.lock.release()

            while wait_to_ready and not module.is_ready():
                pass

            return module

        except:
            traceback.print_exc()
            return None

        finally:
            if self.lock.locked():
                self.lock.release()

    def get_module(self, module_name):
        try:
            return self.modules.get(module_name)

        except:
            traceback.print_exc()
            return None

    def get_all_modules(self):
        try:
            return self.modules.copy()

        except:
            traceback.print_exc()
            return None

    def run_module(self, module_name, inputs=None):
        try:
            module = self.get_module(module_name)
            if module == None:
                return None

            return module.run(inputs=inputs)

        except:
            traceback.print_exc()
            return None


class MAPE:
    def __init__(self, system, period=60):
        self.system = system
        self.period = period
        self.MAPE_thread = threading.Thread(target=self.MAPE)
        self.is_start_flag = False
        self.is_stop_flag = False

    def create(system, period=60):
        if period <= 0:
            return None

        return MAPE(system, period=period)

    def start(self):
        self.MAPE_thread.start()
        self.is_start_flag = True

    def is_start(self):
        return self.is_start_flag

    def stop(self):
        self.is_stop_flag = True

    def is_stop(self):
        return self.is_stop_flag

    def flush_pending_modules(self):
        self.system.lock.acquire()

        for pend_module in self.system.pending_modules:
            self.system.modules.get(pend_module).is_ready_flag = True

        self.system.pending_modules = list()

        self.system.lock.release()

    def MAPE(self):
        try:
            i = 1
            while not self.is_stop_flag:

                time.sleep(self.period)

                print(f"start MAPE round {i}")

                self.flush_pending_modules()

                for module_name, module in self.system.modules.items():
                    monitor = module.monitor()
                    analyse = module.analyse(monitor)
                    planning = module.planning(analyse)
                    module.execute(planning)

                print(f"finish MAPE round {i}")
                i += 1

        except:
            self.MAPE_thread = threading.Thread(target=self.MAPE)
            self.MAPE_thread.start()

            traceback.print_exc()
            return None
