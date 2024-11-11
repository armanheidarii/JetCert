import os
import sys
import threading
import subprocess
import traceback
import time
import json
import queue
import sqlite3
from flask import Flask, request, Response
from http import HTTPStatus


class Builder:
    fast_compilation_tools = ["numba", "codon", "python"]

    def __init__(self, module):
        self.module = module

    def create(module):
        return Builder(module)

    def is_json(input_obj):
        try:
            if type(input_obj) == str:
                json.loads(input_obj)

            else:
                json.dumps(input_obj)

            return True

        except:
            return False

    def importer(name, root_package=False, relative_globals=None, level=0):
        """We only import modules, functions can be looked up on the module.
        Usage:

        from foo.bar import baz
        >>> baz = importer('foo.bar.baz')

        import foo.bar.baz
        >>> foo = importer('foo.bar.baz', root_package=True)
        >>> foo.bar.baz

        from .. import baz (level = number of dots)
        >>> baz = importer('baz', relative_globals=globals(), level=2)
        """

        try:
            return __import__(
                name,
                locals=None,
                globals=relative_globals,
                fromlist=[] if root_package else [None],
                level=level,
            )

        except:
            traceback.print_exc()
            return None

    def extract_relative_paths(file_paths, base_path):
        relative_paths = []
        for file_path in file_paths:
            if base_path in file_path:
                relative_path = os.path.relpath(file_path, base_path)
                relative_paths.append(relative_path)
        return relative_paths

    def create_db(path):
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, "Database.db")
        return sqlite3.connect(path, check_same_thread=False)

    def compile_numba_versions(self):
        files_path = self.module.get_numba_files_path()
        for name, file_path in files_path.items():
            numba_entry_module = Builder.importer(file_path)
            numba_entry_function = getattr(
                numba_entry_module, self.module.fast_numba_entry_func_name
            )

            self.module.numba_cache_functions[name] = numba_entry_function

    def compile_codon_versions(self):
        files_path = self.module.get_state_files_path("fast")
        for file_path in files_path:
            base_cmd = ["codon", "build", "-release", "-exe", f"{file_path}.py"]
            response = Builder.run_cmd(base_cmd)

            print(response)

    def compile_fast_versions(self):
        if self.module.fast_compilation_tool == "numba":
            self.compile_numba_versions()
        elif self.module.fast_compilation_tool == "codon":
            self.compile_codon_versions()

    def compile_safe_versions(self):
        files_path = self.module.get_state_files_path("safe")
        for name, file_path in files_path.items():

            base_cmd = ["gcc", f"{file_path}.c"]
            linked_cmd = [
                f"-l{linked_file}" for linked_file in self.module.safe_linked_files
            ]
            output_cmd = ["-o", file_path]
            cmd = base_cmd + linked_cmd + output_cmd
            response = Builder.run_cmd(cmd)

            print(response)

    def run_cmd(cmd, dest_path=".", inputs=None):
        original_path = os.getcwd()
        try:
            os.chdir(dest_path)
        except:
            # None nade va json bede
            return None

        if inputs != None:
            inputs = json.dumps(inputs) if Builder.is_json(inputs) else f"{inputs}"

        completed_process = subprocess.run(
            cmd,
            input=inputs,
            capture_output=True,
            text=True,
        )

        os.chdir(original_path)

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

    def run_numba_file(self, name, inputs=None):
        response = {}

        try:
            response["returncode"] = 0
            stdout = (
                self.module.numba_cache_functions.get(name)()
                if inputs == None
                else self.module.numba_cache_functions.get(name)(inputs)
            )
            response["stdout"] = (
                json.dumps(stdout) if Builder.is_json(stdout) else f"{stdout}"
            )
            response["stderr"] = ""

        except:
            response["returncode"] = 1
            response["stdout"] = ""
            response["stderr"] = traceback.format_exc()

        response["args"] = "JIT execution"

        stdout = response.get("stdout")
        return {
            "process": response,
            "result": (json.loads(stdout) if Builder.is_json(stdout) else stdout),
        }

    def git_pull(path=".", remote_name="origin", branch="main"):
        cmd = ["git", "pull", remote_name, branch]
        response = Builder.run_cmd(cmd, dest_path=path)
        return response.get("returncode") == 0

    def get_git_head_hash(path="."):
        cmd = ["git", "rev-parse", "HEAD"]
        response = Builder.run_cmd(cmd, dest_path=path)
        if response.get("returncode") != 0:
            return None

        return response.get("stdout").strip()

    def get_git_file_changes(git_head_hash, path="."):
        cmd = f"""GIT_PAGER=cat && git log --pretty=format:"%H" --no-patch | while read -r itr; do if [ "$itr" != "{git_head_hash}" ]; then git diff --name-only $itr; else break; fi; done | sort |  uniq"""
        response = Builder.run_cmd(cmd, dest_path=path)
        return response.get("stdout")


class Module:
    def __init__(
        self,
        system,
        module_name,
        fast_compilation_tool="python",
        fast_entry_file_name="__main__",
        fast_numba_entry_func_name="go_fast",
        safe_entry_file_name="main",
        safe_linked_files=[],
    ):
        self.system = system
        self.module_name = module_name
        self.fast_compilation_tool = fast_compilation_tool
        self.fast_entry_file_name = fast_entry_file_name
        self.fast_numba_entry_func_name = fast_numba_entry_func_name
        self.safe_entry_file_name = safe_entry_file_name
        self.safe_linked_files = safe_linked_files
        self.is_ready_flag = False
        self.is_active_flag = True
        self.safety = {"state": "safe", "level": 1}
        self.numba_cache_functions = {}
        self.requests_number = 0
        self.builder = Builder.create(self)

    def create(
        system,
        module_name,
        fast_compilation_tool="python",
        fast_entry_file_name="__main__",
        fast_numba_entry_func_name="go_fast",
        safe_entry_file_name="main",
        safe_linked_files=[],
    ):

        if not fast_compilation_tool in Builder.fast_compilation_tools:
            return None

        module = Module(
            system,
            module_name,
            fast_compilation_tool=fast_compilation_tool,
            fast_entry_file_name=fast_entry_file_name,
            fast_numba_entry_func_name=fast_numba_entry_func_name,
            safe_entry_file_name=safe_entry_file_name,
            safe_linked_files=safe_linked_files,
        )

        module.builder.compile_fast_versions()
        module.builder.compile_safe_versions()

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
        try:
            return (
                ("active" if self.is_active_flag else "inactive")
                if self.is_ready_flag
                else "pending"
            )
        except:
            traceback.print_exc()
            return None

    def get_safety(self):
        return self.safety.copy()

    def get_requests_number(self):
        try:
            return self.requests_number

        except:
            traceback.print_exc()
            return None

    def run(self, inputs=None):
        try:
            if not self.is_ready() or not self.is_active():
                return None

            safety = self.safety.copy()
            safety_state = safety.get("state")
            safety_level = safety.get("level")

            file_path = self.get_file_path(safety_state, safety_level)

            response = None
            if safety_state == "fast":

                if self.fast_compilation_tool == "numba":
                    response = self.builder.run_numba_file(
                        f"level{safety_level}", inputs=inputs
                    ).copy()

                elif self.fast_compilation_tool == "codon":
                    response = Builder.run_exe_file(file_path, inputs=inputs).copy()

                elif self.fast_compilation_tool == "python":
                    response = Builder.run_python_file(
                        f"{file_path}.py", inputs=inputs
                    ).copy()

            elif safety_state == "safe":
                response = Builder.run_exe_file(file_path, inputs=inputs).copy()

            response["safety"] = safety

            self.requests_number += 1

            return response

        except:
            traceback.print_exc()
            return None

    def execute(self, planning_data):
        try:
            self.safety = planning_data

        except:
            traceback.print_exc()

    def get_module_path(self):
        modules_path = self.system.get_modules_path()
        return f"{modules_path}/{self.module_name}"

    def get_state_path(self, safety_state):
        module_path = self.get_module_path()
        return f"{module_path}/{safety_state}"

    def get_level_path(self, safety_state, safety_level):
        state_path = self.get_state_path(safety_state)
        return f"{state_path}/level{safety_level}"

    def get_file_path(self, safety_state, safety_level):
        level_path = self.get_level_path(safety_state, safety_level)

        entry_file_name = (
            self.fast_entry_file_name
            if safety_state == "fast"
            else self.safe_entry_file_name
        )

        return f"{level_path}/{entry_file_name}"

    def get_state_files_path(self, safety_state):
        state_path = self.get_state_path(safety_state)

        state_levels_path = {}
        for name in os.listdir(state_path):
            if name.startswith("level"):
                file_path = self.get_file_path(
                    safety_state, int(name[name.rfind("l") + 1 :])
                )
                state_levels_path[name] = file_path

        return state_levels_path

    def get_numba_file_path(self):
        file_path = self.get_file_path(safety_state, safety_level)
        return file_path[file_path.rfind(self.module_name) :].replace("/", ".")

    def get_numba_files_path(self):
        return {
            name: file_path[file_path.rfind(self.module_name) :].replace("/", ".")
            for name, file_path in self.get_state_files_path("fast").items()
        }

    def __str__(self):
        safety = self.safety.copy()
        safety_state = safety.get("state")
        safety_level = safety.get("level")

        return f"<Module {self.module_name} ({self.get_status()}) in state {safety_state} and level {safety_level}>"


class JetCert:
    def __init__(
        self,
        period=60,
        modules_path=".",
        capture_MAPE_data=False,
        MAPE_data_path=".",
        github_webhook_port=8085,
        github_webhook_path="/update",
        github_webhook_secret="",
    ):
        self.modules_path = modules_path
        self.modules = dict()
        self.pending_modules_name = list()
        self.MAPE = MAPE.create(
            self,
            period=period,
            capture_MAPE_data=capture_MAPE_data,
            MAPE_data_path=MAPE_data_path,
        )
        self.CI = CI.create(
            self,
            github_webhook_port=github_webhook_port,
            github_webhook_path=github_webhook_path,
            github_webhook_secret=github_webhook_secret,
        )
        self.lock = threading.Lock()

    def create(
        period=60,
        modules_path=".",
        capture_MAPE_data=False,
        MAPE_data_path=".",
        github_webhook_port=8085,
        github_webhook_path="/update",
        github_webhook_secret="",
    ):
        try:
            if period <= 0:
                return None

            modules_path = os.path.abspath(modules_path)
            sys.path.append(modules_path)

            jetCert = JetCert(
                period=period,
                modules_path=modules_path,
                capture_MAPE_data=capture_MAPE_data,
                MAPE_data_path=MAPE_data_path,
                github_webhook_port=github_webhook_port,
                github_webhook_path=github_webhook_path,
                github_webhook_secret=github_webhook_secret,
            )

            is_webhook_set = jetCert.CI.set_webhook()

            if not is_webhook_set:
                return None

            return jetCert
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
        fast_compilation_tool="python",
        fast_entry_file_name="__main__",
        fast_numba_entry_func_name="go_fast",
        safe_entry_file_name="main",
        safe_linked_files=[],
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
                fast_compilation_tool=fast_compilation_tool,
                fast_entry_file_name=fast_entry_file_name,
                fast_numba_entry_func_name=fast_numba_entry_func_name,
                safe_entry_file_name=safe_entry_file_name,
                safe_linked_files=safe_linked_files,
            )

            self.modules[module_name] = module
            self.pending_modules_name.append(module_name)

            self.lock.release()

            while self.is_start() and wait_to_ready and not module.is_ready():
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

    def get_MAPE_data(self, limit=-1, offset=0, wait_to_ready=False):
        try:
            return self.MAPE.get_MAPE_data(
                limit=limit,
                offset=offset,
                wait_to_ready=wait_to_ready,
            )

        except:
            traceback.print_exc()
            return None

    def get_MAPE_data_path(self):
        try:
            return self.MAPE.get_MAPE_data_path()

        except:
            traceback.print_exc()
            return None

    def get_modules_path(self):
        try:
            return self.modules_path

        except:
            traceback.print_exc()
            return None


class MAPE:
    def __init__(self, system, period=60, capture_MAPE_data=False, MAPE_data_path="."):
        self.system = system
        self.period = period
        self.capture_MAPE_data = capture_MAPE_data
        self.MAPE_data_path = MAPE_data_path
        self.is_start_flag = False
        self.is_stop_flag = False
        self.conn = None
        self.cursor = None
        self.itr = 0

    def create(system, period=60, capture_MAPE_data=False, MAPE_data_path="."):
        if period <= 0:
            return None

        return MAPE(
            system,
            period=period,
            capture_MAPE_data=capture_MAPE_data,
            MAPE_data_path=MAPE_data_path,
        )

    def create_MAPE_db(self):
        self.conn = Builder.create_db(self.MAPE_data_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS MAPE (
                Monitor real, 
                Analyse real, 
                Planning real, 
                Execute real, 
                Overall real, 
                Safe_Interval real)"""
        )
        self.conn.commit()

    def setup_itr(self):
        self.cursor.execute("SELECT COUNT(*) FROM MAPE")
        self.itr = self.cursor.fetchone()[0]

    def start(self):
        if self.is_capture_MAPE_data():
            self.create_MAPE_db()
            self.setup_itr()

        print(f"start MAPE round 0")

        self.update()

        print(f"finish MAPE round 0")

        threading.Thread(target=self.MAPE).start()
        self.is_start_flag = True

    def is_start(self):
        return self.is_start_flag

    def stop(self):
        self.conn.close()
        self.is_stop_flag = True

    def is_stop(self):
        return self.is_stop_flag

    def is_capture_MAPE_data(self):
        return self.capture_MAPE_data

    def monitor(self):
        try:
            start = time.time()

            monitor_file_path = self.get_mape_file_path("monitor")
            response = Builder.run_python_file(monitor_file_path)
            print(response)
            end = time.time()

            return response.get("result"), end - start

        except:
            traceback.print_exc()
            return None, None

    def analyse(self, monitor_data):
        try:
            start = time.time()

            analyse_file_path = self.get_mape_file_path("analyse")
            response = Builder.run_python_file(analyse_file_path, inputs=monitor_data)

            end = time.time()

            return response.get("result"), end - start

        except:
            traceback.print_exc()
            return None, None

    def planning(self, analyse_data):
        try:
            start = time.time()

            planning_file_path = self.get_mape_file_path("planning")
            response = Builder.run_python_file(planning_file_path, inputs=analyse_data)

            end = time.time()

            return response.get("result"), end - start

        except:
            traceback.print_exc()
            return None, None

    def execute(self, planning_data):
        try:
            start = time.time()

            for module_name, data in planning_data.items():
                module = self.system.modules.get(module_name)
                if module != None:
                    module.execute(data)

            end = time.time()

            return end - start

        except:
            traceback.print_exc()
            return None, None

    def active_pending_modules(self):
        for pend_module_name in self.system.pending_modules_name:
            self.system.modules.get(pend_module_name).is_ready_flag = True

            if self.is_capture_MAPE_data():
                self.cursor.execute(
                    f"""CREATE TABLE IF NOT EXISTS {pend_module_name} (
                        Status TEXT, 
                        State TEXT, 
                        Level INTEGER)"""
                )
                self.conn.commit()

        self.system.pending_modules_name = list()

    def update(self):
        self.system.lock.acquire()

        monitor, monitor_execution_time = self.monitor()
        analyse, analyse_execution_time = self.analyse(monitor)
        planning, planning_execution_time = self.planning(analyse)
        execute_execution_time = self.execute(planning)

        if self.is_capture_MAPE_data():

            overall_execution_time = (
                monitor_execution_time
                + analyse_execution_time
                + planning_execution_time
                + execute_execution_time
            )
            safe_interval = self.period - overall_execution_time

            data = (
                monitor_execution_time,
                analyse_execution_time,
                planning_execution_time,
                execute_execution_time,
                overall_execution_time,
                safe_interval,
            )

            self.cursor.execute(f"INSERT INTO MAPE VALUES {data}")
            self.conn.commit()

        self.active_pending_modules()

        self.itr += 1

        self.system.lock.release()

    def CI_queue_updating(self):
        queue = self.system.CI.queue

        start_time = time.time()
        while time.time() - start_time < self.period:
            if not queue.empty():
                element = queue.get()
                module_name = element.get("module_name")
                module = self.system.modules[module_name]
                safety = element.get("safety")
                level = element.get("level")
                print(element)

    def MAPE(self):
        try:
            while not self.is_stop_flag:

                self.CI_queue_updating()

                print(f"start MAPE round {self.itr}")

                self.update()

                print(f"finish MAPE round {self.itr}")

        except:
            threading.Thread(target=self.MAPE).start()

            traceback.print_exc()
            return None

    def get_MAPE_data(self, limit=-1, offset=0, wait_to_ready=False):
        if not self.is_start() or not self.is_capture_MAPE_data():
            return None

        if (limit < 0 and limit != -1) or offset < 0:
            return None

        while wait_to_ready and self.itr <= limit + offset:
            pass

        self.cursor.execute("SELECT * FROM MAPE LIMIT ? OFFSET ?", (limit, offset))

        MAPE_data = self.cursor.fetchall()
        monitor_execution_times = [row[0] for row in MAPE_data]
        analyse_execution_times = [row[1] for row in MAPE_data]
        planning_execution_times = [row[2] for row in MAPE_data]
        execute_execution_times = [row[3] for row in MAPE_data]
        overall_execution_times = [row[4] for row in MAPE_data]
        safe_intervals = [row[5] for row in MAPE_data]

        return {
            "iterations_count": len(monitor_execution_times),
            "monitor_execution_times": monitor_execution_times,
            "analyse_execution_times": analyse_execution_times,
            "planning_execution_times": planning_execution_times,
            "execute_execution_times": execute_execution_times,
            "overall_execution_times": overall_execution_times,
            "safe_intervals": safe_intervals,
        }

    def get_mape_file_path(self, file_name):
        modules_path = self.system.get_modules_path()
        return f"{modules_path}/__MAPE__/{file_name}"

    def get_MAPE_data_path(self):
        return self.MAPE_data_path


class CI:
    def __init__(
        self,
        system,
        github_webhook_port=8085,
        github_webhook_path="/update",
        github_webhook_secret="",
    ):
        self.system = system
        self.queue = queue.Queue()
        self.app = Flask(__name__)
        self.github_webhook_port = github_webhook_port
        self.github_webhook_path = github_webhook_path
        self.github_webhook_secret = github_webhook_secret
        self.git_head_hash = None

    def create(
        system,
        github_webhook_port=8085,
        github_webhook_path="/update",
        github_webhook_secret="",
    ):
        return CI(
            system,
            github_webhook_port=github_webhook_port,
            github_webhook_path=github_webhook_path,
            github_webhook_secret=github_webhook_secret,
        )

    def create_queue_elements(relative_changed_files):
        queue_elements = []
        for relative_changed_file in relative_changed_files:
            parts = relative_changed_file.split("/")

            queue_elements.append(
                {
                    "module_name": parts[0],
                    "safety": parts[1],
                    "level": parts[2],
                }
            )

        return queue_elements

    def put_queue_elements(self, queue_elements):
        for queue_element in queue_elements:
            self.queue.put(queue_element)

    def verify_signature(self, payload, signature):
        computed_signature = (
            "sha256="
            + hmac.new(
                self.github_webhook_secret.encode(),
                payload,
                hashlib.sha256,
            ).hexdigest()
        )
        return hmac.compare_digest(computed_signature, signature)

    def webhook_handler(self):
        signature = request.headers.get("X-Hub-Signature-256")
        if not signature:
            Response("Missing signature", status=HTTPStatus.BadRequest)

        if not self.verify_signature(request.data, signature):
            Response("Invalid signature", status=HTTPStatus.FORBIDDEN)

        event = request.headers.get("X-GitHub-Event")
        print(f"Received event: {event}")

        if event == "push":
            print("Push event received")
        elif event == "pull_request":
            print("Pull request event received")

        is_git_pull = Builder.git_pull(self.system.get_modules_path())
        if is_git_pull:
            return Response("Can not updated", status=HTTPStatus.INTERNAL_SERVER_ERROR)

        changed_files = Builder.get_git_file_changes(self.git_head_hash)

        relative_changed_files = Builder.extract_relative_paths(changed_files)
        queue_elements = CI.create_queue_elements(relative_changed_files)
        self.put_queue_elements(queue_elements)

        modules_path = self.system.get_modules_path()
        self.git_head_hash = Builder.get_git_head_hash(modules_path)

        return Response("Updated", status=HTTPStatus.OK)

    def set_webhook(self):
        @self.app.route(self.github_webhook_path, methods=["POST"])
        def webhook():
            return self.webhook_handler()

        run_thread = threading.Thread(
            target=self.app.run,
            kwargs={"host": "0.0.0.0", "port": self.github_webhook_port},
        )
        run_thread.start()

        time.sleep(1)

        if not run_thread.is_alive():
            return False

        return True
