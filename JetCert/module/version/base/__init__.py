import os
from enum import Enum


class CompilationModeTypes(Enum):
    FAST = "fast"
    SAFE = "safe"


class BaseVersion:
    def __init__(self, module, version_name):
        if not module:
            raise ValueError(f"The module {module} cannot be empty!")
        self.module = module

        module_path = module.get_module_path()
        version_path = os.path.join(module_path, version_name)
        if not os.path.exists(version_path):
            raise ValueError(f"The version_path {version_path} does not exist!")
        self.version_path = version_path

        config_file_path = os.path.join(version_path, module.system.config_files_name)
        if not os.path.exists(config_file_path):
            raise ValueError(f"The config_file_path {config_file_path} does not exist!")
        self.config_file_path = config_file_path

        self.version_name = version_name
        self.compiles_number = 0
        self.requests_number = 0

    def get_module(self):
        return self.module

    def get_module_name(self):
        return self.module.get_module_name()

    def get_version_path(self):
        return self.version_path

    def get_config_file_path(self):
        return self.config_file_path

    def get_config_files_name(self):
        return self.module.system.config_files_name

    def get_version_name(self):
        return self.version_name

    def get_requests_number(self):
        return self.requests_number

    def get_compiles_number(self):
        return self.compiles_number

    def compile(self):
        self.compiles_number += 1

    def run(self, inputs=None):
        self.requests_number += 1

    def sign(self, response):
        if not response:
            raise ValueError(f"The response {response} cannot be empty!")

        if type(response) != dict:
            raise ValueError(f"The response {response} is not dict!")

        response["version_name"] = self.version_name
        return response

    def __str__(self):
        return f"<Version {self.version_name} in {self.compilation_mode} mode with {self.compilation_tool} tool>"
