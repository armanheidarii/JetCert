import os

from utils import Utils
from module.version.base import BaseVersion
from module.version.base import CompilationModeTypes


class SafeVersion(BaseVersion):
    def __init__(self, module, version_name, compilation_mode_config):
        super().__init__(module, version_name)

        if not compilation_mode_config:
            raise Exception(
                f"The compilation_mode config {compilation_mode_config} cannot be empty!"
            )

        self.compilation_mode = CompilationModeTypes.SAFE
        self.entry_file_name = "main.c"

        entry_file_name = compilation_mode_config.get("entry_file_name")
        if entry_file_name:
            if not Utils.is_valid_c_filename(entry_file_name):
                raise Exception(
                    f"The entry_file_name {entry_file_name} is not the name of a c file!"
                )
            self.entry_file_name = entry_file_name

        version_path = self.get_version_path()
        entry_file_path = os.path.join(version_path, self.entry_file_name)
        if not os.path.exists(entry_file_path):
            raise Exception(f"The entry_file_path {entry_file_path} does not exist!")
        self.entry_file_path = entry_file_path

    def get_compilation_mode(self):
        return self.compilation_mode

    def get_entry_file_name(self):
        return self.entry_file_name

    def get_entry_file_path(self):
        return self.entry_file_path

    def __str__(self):
        version_name = self.get_version_name()
        return f"<Safe Version {version_name} with {self.compilation_tool} tool>"
