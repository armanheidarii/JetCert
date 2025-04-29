import os
import traceback
import subprocess
import json

from utils import Utils


class Builder:
    @staticmethod
    def run_cmd(cmd, path=".", inputs=None):
        try:
            original_path = os.getcwd()
            os.chdir(path)

            if inputs != None:
                inputs = json.dumps(inputs) if Utils.is_json(inputs) else f"{inputs}"

            completed_process = subprocess.run(
                cmd,
                input=inputs,
                shell=True,
                capture_output=True,
                text=True,
            )

            os.chdir(original_path)

            return {
                "process": {
                    "returncode": completed_process.returncode,
                    "stdout": completed_process.stdout,
                    "stderr": completed_process.stderr,
                    "args": completed_process.args,
                },
                "result": completed_process.stdout,
            }

        except Exception as e:
            return {
                "process": {
                    "returncode": 1,
                    "stdout": "",
                    "stderr": traceback.format_exc(),
                    "args": cmd,
                },
                "result": "",
            }

    @classmethod
    def compile_compcert_file(cls, entry_file_path, linked_files=[]):
        entry_base_file_path = Utils.get_base_file_path(entry_file_path)
        base_cmd = f"""./builder/CompCert/ccomp {entry_file_path}"""
        linked_cmd = " ".join([f"-l{linked_file}" for linked_file in linked_files])
        output_cmd = f"""-o {entry_base_file_path}"""
        cmd = f"""{base_cmd} {linked_cmd} {output_cmd}"""
        return cls.run_cmd(cmd)

    @classmethod
    def compile_codon_file(cls, entry_file_path):
        base_cmd = f"""codon build -release -exe {entry_file_path}"""
        return cls.run_cmd(base_cmd)

    @staticmethod
    def compile_numba_file(entry_file_path, entry_func_name="go_fast"):
        try:
            entry_base_file_path = Utils.get_base_file_path(entry_file_path)
            relative_entry_base_file_path = entry_base_file_path.split("modules")[
                -1
            ].lstrip(os.sep)
            modular_entry_base_file_path = relative_entry_base_file_path.replace(
                "/", "."
            )
            entry_module = Utils.importer(modular_entry_base_file_path)
            entry_function = getattr(entry_module, entry_func_name)

            return {
                "process": {
                    "returncode": 0,
                    "stdout": "",
                    "stderr": "",
                    "args": "compile numba file",
                },
                "result": entry_function,
            }

        except Exception as e:
            return {
                "process": {
                    "returncode": 1,
                    "stdout": "",
                    "stderr": traceback.format_exc(),
                    "args": "compile numba file",
                },
                "result": "",
            }

    @classmethod
    def run_exe_file(cls, entry_file_path, inputs=None):
        cmd = f"""{entry_file_path}"""
        response = cls.run_cmd(cmd, inputs=inputs)

        process = response.get("process")
        result = response.get("result")
        return {
            "process": process,
            "result": (json.loads(result) if Utils.is_json(result) else result),
        }

    @classmethod
    def run_python_file(cls, entry_file_path, inputs=None):
        cmd = f"""python3 {entry_file_path}"""
        response = cls.run_cmd(cmd, inputs=inputs)

        process = response.get("process")
        result = response.get("result")
        return {
            "process": process,
            "result": (json.loads(result) if Utils.is_json(result) else result),
        }

    @staticmethod
    def run_numba_func(cache_function, inputs=None):
        try:
            stdout = cache_function() if inputs == None else cache_function(inputs)

            return {
                "process": {
                    "returncode": 0,
                    "stdout": f"{stdout}",
                    "stderr": "",
                    "args": "run numba func",
                },
                "result": stdout,
            }

        except Exception as e:
            return {
                "process": {
                    "returncode": 1,
                    "stdout": "",
                    "stderr": traceback.format_exc(),
                    "args": "run numba func",
                },
                "result": "",
            }

    @classmethod
    def git_pull(cls, path=".", remote_name="origin", branch="main"):
        cmd = f"""git pull {remote_name} {branch}"""
        return cls.run_cmd(cmd, path=path)

    @classmethod
    def get_git_head_hash(cls, path="."):
        cmd = """git rev-parse HEAD"""
        return cls.run_cmd(cmd, path=path)

    @classmethod
    def get_git_files_changes(cls, prev_git_head_hash, path="."):
        cmd = f"""git log --name-status --pretty="format:" {prev_git_head_hash}..HEAD | awk '{{print $2}}' | grep -v '^$' | sort | uniq"""
        return cls.run_cmd(cmd, path=path)
