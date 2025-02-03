import os
import sys

sys.path.append("JetCert")

from utils import Utils
from module import Module
from mape import MAPE
from cd import CD


class JetCert:
    def __init__(
        self,
        period=60,
        modules_path=".",
        config_files_name="config.toml",
        continuous_deployment=False,
    ):
        if not os.path.exists(modules_path):
            raise ValueError(f"The modules_path {modules_path} does not exist!")
        self.modules_path = os.path.abspath(modules_path)

        sys.path.append(modules_path)

        self.cache_folder_name = "__jetcert__"

        config_files_basename, config_files_extension = os.path.splitext(
            config_files_name
        )
        if config_files_extension != ".toml":
            raise ValueError(
                f"The config_files_name {config_files_name} is not a toml file!"
            )
        self.config_files_name = config_files_name

        self.is_start_flag = False
        self.modules = dict()

        cache_folder_path = os.path.join(self.modules_path, self.cache_folder_name)
        os.makedirs(cache_folder_path, exist_ok=True)
        self.cache_folder_path = cache_folder_path

        Utils.clear_folder(self.cache_folder_path)

        self.MAPE = MAPE(self, period=period)
        self.CD = CD(self, continuous_deployment)

        self.parse()

    def get_modules_path(self):
        return self.modules_path

    def get_cache_folder_name(self):
        return self.cache_folder_name

    def get_config_files_name(self):
        return self.config_files_name

    def get_cache_folder_path(self):
        return self.cache_folder_path

    def get_base_model(self):
        return self.base_model

    def is_start(self):
        return self.is_start_flag

    def is_module_exist(self, module_name):
        return module_name in self.modules

    def get_module(self, module_name):
        return self.modules.get(module_name)

    def get_all_modules(self):
        return self.modules.copy()

    def get_MAPE(self):
        return self.MAPE

    def get_period(self):
        return self.MAPE.get_period()

    def get_CD(self):
        return self.CD

    def is_continuous_deployment_active(self):
        return self.CD.is_continuous_deployment_active()

    def parse_modules(self):
        modules_list = Utils.list_folders(self.modules_path)
        if not modules_list:
            raise ValueError(f"The modules_path {self.modules_path} has no module!")

        if "__pycache__" in modules_list:
            modules_list.remove("__pycache__")

        cache_folder_name = self.get_cache_folder_name()
        if cache_folder_name in modules_list:
            modules_list.remove(cache_folder_name)

        MAPE_folder_name = self.MAPE.get_MAPE_folder_name()
        if MAPE_folder_name in modules_list:
            modules_list.remove(MAPE_folder_name)

        for module_name in modules_list:
            self.add_module(module_name)

    def parse(self):
        self.parse_modules()

    def add_module(self, module_name):
        self.modules[module_name] = Module(self, module_name)
        return self.modules[module_name]

    def compile_module(self, module_name):
        if not self.is_start_flag:
            raise ValueError(f"The system {self} not started!")

        module = self.get_module(module_name)
        if not module:
            raise ValueError(f"The module_name {module_name} not found!")

        self.compiles_number += 1

        return module.compile()

    def compile_all_modules(self):
        if not self.is_start_flag:
            raise ValueError(f"The system {self} not started!")

        responses = []

        for module in self.modules.values():
            self.compiles_number += 1

            response = module.compile()
            responses.append(response)

        return responses

    def run_module(self, module_name, inputs=None):
        if not self.is_start_flag:
            raise ValueError(f"The system {self} not started!")

        module = self.get_module(module_name)
        if not module:
            raise ValueError(f"The module_name {module_name} not found!")

        return module.run(inputs=inputs)

    def execute_module(self, module_name, current_version_name):
        if not self.is_module_exist(module_name):
            raise ValueError(f"The module_name {module_name} not found!")

        module = self.get_module(module_name)
        module.execute(current_version_name)

    def update_CD(self):
        self.CD.update()

    def start(self):
        self.MAPE.start()

        if self.CD.is_continuous_deployment_active():
            self.CD.start()

        self.is_start_flag = True

    def __str__(self):
        period = self.MAPE.get_period()
        MAPE_status = "start" if self.is_start_flag else "not start"
        is_continuous_deployment_active = (
            "active" if self.CD.is_continuous_deployment_active() else "inactive"
        )
        return f"<JetCert ({MAPE_status}) in period {period} with {is_continuous_deployment_active}>"
