import os
from enum import Enum

from utils import Utils
from module.version.base import BaseVersion
from module.version.base import CompilationModeTypes


class FastCompilationToolTypes(Enum):
    NUMBA = "numba"
    CODON = "codon"
    PYTHON = "python"


class FastVersion(BaseVersion):
    def __init__(self, module, version_name, compilation_mode_config):
        super().__init__(module, version_name)

        if not compilation_mode_config:
            raise ValueError(
                f"The compilation_mode_config {compilation_mode_config} cannot be empty!"
            )

        self.compilation_mode = CompilationModeTypes.FAST
        self.entry_file_name = "__main__.py"

        entry_file_name = compilation_mode_config.get("entry_file_name")
        if entry_file_name:
            if not Utils.is_valid_python_filename(entry_file_name):
                raise ValueError(
                    f"The entry_file_name {entry_file_name} is not the name of a python file!"
                )
            self.entry_file_name = entry_file_name

        version_path = self.get_version_path()
        entry_file_path = os.path.join(version_path, self.entry_file_name)
        if not os.path.exists(entry_file_path):
            raise ValueError(f"The entry_file_path {entry_file_path} does not exist!")
        self.entry_file_path = entry_file_path

    def get_compilation_mode(self):
        return self.compilation_mode

    def get_entry_file_name(self):
        return self.entry_file_name

    def get_entry_file_path(self):
        return self.entry_file_path

    def __str__(self):
        version_name = self.get_version_name()
        return f"<Fast Version {version_name} with {self.compilation_tool} tool>"
