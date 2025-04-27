import os

from utils import Utils
from module.version import Version
from module.version.base import CompilationModeTypes
from module.version.base.fast import FastCompilationToolTypes
from module.version.base.safe import SafeCompilationToolTypes


class Module:
    def __init__(self, system, module_name):
        if not system:
            raise Exception(f"The system {system} cannot be empty!")
        self.system = system

        modules_path = self.system.get_modules_path()
        module_path = os.path.join(modules_path, module_name)
        if not os.path.exists(module_path):
            raise Exception(f"The module_path {module_path} does not exist!")
        self.module_path = module_path

        self.module_name = module_name
        self.versions = dict()
        self.current_version_name = None
        self.compiles_number = 0
        self.requests_number = 0

        self.parse()

    def get_system(self):
        return self.system

    def get_module_path(self):
        return self.module_path

    def get_config_files_name(self):
        return self.system.config_files_name

    def get_module_name(self):
        return self.module_name

    def is_version_exist(self, version_name):
        return version_name in self.versions

    def get_version(self, version_name):
        return self.versions.get(version_name)

    def get_all_versions(self):
        return self.versions.copy()

    def get_current_version_name(self):
        return self.current_version_name

    def get_requests_number(self):
        return self.requests_number

    def get_compiles_number(self):
        return self.compiles_number

    def parse_versions(self):
        versions_list = Utils.list_folders(self.module_path)
        if not versions_list:
            raise Exception(f"The module_path {self.module_path} has no version!")

        if "__pycache__" in versions_list:
            versions_list.remove("__pycache__")

        cache_folder_name = self.system.get_cache_folder_name()
        if cache_folder_name in versions_list:
            versions_list.remove(cache_folder_name)

        for version_name in versions_list:
            version = self.add_version(version_name)
            version.compile()

    def parse(self):
        self.parse_versions()

    def add_version(self, version_name):
        self.versions[version_name] = Version.create(self, version_name)
        return self.versions[version_name]

    def compile_version(self, version_name):
        version = self.get_version(version_name)
        if not version:
            raise Exception(f"The version_name {version_name} not found!")

        self.compiles_number += 1

        return version.compile()

    def compile_tool_versions(self, tool_type):
        if (
            tool_type not in FastCompilationToolTypes
            and tool_type not in SafeCompilationToolTypes
        ):
            raise Exception(
                f"The tool_type {tool_type} is not FastCompilationTool or SafeCompilationTool!"
            )

        responses = []

        for version_name, version in self.versions.items():
            if version.compilation_tool == tool_type:
                self.compiles_number += 1

                response = version.compile()
                responses.append(response)

        return responses

    def compile_mode_versions(self, mode_type):
        if mode_type not in CompilationModeTypes:
            raise Exception(f"The mode_type {mode_type} is not CompilationMode!")

        responses = []

        for version_name, version in self.versions.items():
            if version.compilation_mode == mode_type:
                self.compiles_number += 1

                response = version.compile()
                responses.append(response)

        return responses

    def compile_all_versions(self):
        responses = []

        for version in self.versions.values():
            self.compiles_number += 1

            response = version.compile()
            responses.append(response)

        return responses

    def compile_numba_versions(self):
        return self.compile_tool_versions(FastCompilationToolTypes.NUMBA)

    def compile_codon_versions(self):
        return self.compile_tool_versions(FastCompilationToolTypes.CODON)

    def compile_compcert_versions(self):
        return self.compile_tool_versions(SafeCompilationToolTypes.COMPCERT)

    def compile_fast_versions(self):
        return self.compile_mode_versions(CompilationModeTypes.FAST)

    def compile_safe_versions(self):
        return self.compile_mode_versions(CompilationModeTypes.SAFE)

    def run_version(self, version_name, inputs=None):
        version = self.get_version(version_name)
        if not version:
            raise Exception(f"The version_name {version_name} not found!")

        return version.run(inputs=inputs)

    def compile(self):
        if not self.system.is_start():
            raise Exception(f"The system {self} not started!")

        return self.compile_version(self.current_version_name)

    def run(self, inputs=None):
        if not self.system.is_start():
            raise Exception(f"The system {self} not started!")

        self.requests_number += 1

        return self.run_version(self.current_version_name, inputs=inputs)

    def execute(self, current_version_name):
        if not self.is_version_exist(current_version_name):
            raise Exception(
                f"The current_version_name {current_version_name} not found!"
            )

        self.current_version_name = current_version_name

    def log_versions(self, before_each="", after_each=""):
        for version in self.versions.values():
            self.system.logger.info(f"{before_each}{version}{after_each}")

    def __str__(self):
        version_str = (
            ""
            if not self.current_version_name
            else f" in version {self.current_version_name}"
        )

        return f"<Module {self.module_name}{version_str}>"
