import os
import toml

from module.version.base import CompilationModeTypes
from module.version.base.fast import FastCompilationToolTypes
from module.version.base.safe import SafeCompilationToolTypes
from module.version.base.fast.numba import NumbaVersion
from module.version.base.fast.codon import CodonVersion
from module.version.base.fast.python import PythonVersion
from module.version.base.safe.compcert import CompCertVersion


factory = {
    CompilationModeTypes.FAST: {
        FastCompilationToolTypes.NUMBA: NumbaVersion,
        FastCompilationToolTypes.CODON: CodonVersion,
        FastCompilationToolTypes.PYTHON: PythonVersion,
    },
    CompilationModeTypes.SAFE: {SafeCompilationToolTypes.COMPCERT: CompCertVersion},
}


class Version:
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
        self.compilation_mode = None
        self.compilation_tool = None
        self.compilation_mode_config = None
        self.compilation_tool_config = None

        self.parse()

    @staticmethod
    def create(module, version_name):
        version = Version(module, version_name)
        product_cls = factory.get(version.compilation_mode).get(
            version.compilation_tool
        )
        return product_cls(
            version.module,
            version.version_name,
            version.compilation_mode_config,
            version.compilation_tool_config,
        )

    def parse_config_file(self):
        try:
            config = toml.load(self.config_file_path)

        except:
            raise ValueError(
                f"The config file {self.config_file_path} cannot be loaded!"
            )

        if not config:
            raise ValueError(f"The [{self.config_file_path}] cannot be empty!")

        compilation_mode = config.get("compilation_mode")
        if not compilation_mode:
            raise ValueError(
                f"The [{self.config_file_path}].compilation_mode cannot be empty!"
            )
        if compilation_mode not in CompilationModeTypes._value2member_map_.keys():
            raise ValueError(
                f"The [{self.config_file_path}].compilation_mode {compilation_mode} is not CompilationMode!"
            )
        self.compilation_mode = CompilationModeTypes(compilation_mode)

        compilation_mode_config = config.get(self.compilation_mode.value)
        if not compilation_mode_config:
            raise ValueError(
                f"The compilation mode config {compilation_mode_config} cannot be empty!"
            )
        self.compilation_mode_config = compilation_mode_config

        compilation_tool = self.compilation_mode_config.get("compilation_tool")
        if not compilation_tool:
            compilation_tool = (
                FastCompilationToolTypes.NUMBA.value
                if self.compilation_mode == CompilationModeTypes.SAFE
                else SafeCompilationToolTypes.COMPCERT.value
            )
        if (
            self.compilation_mode == CompilationModeTypes.FAST
            and compilation_tool
            not in FastCompilationToolTypes._value2member_map_.keys()
        ):
            raise ValueError(
                f"The [{self.config_file_path}].{self.compilation_mode.value}.compilation_tool {compilation_tool} is not FastCompilationTool!"
            )
        if (
            self.compilation_mode == CompilationModeTypes.SAFE
            and compilation_tool
            not in SafeCompilationToolTypes._value2member_map_.keys()
        ):
            raise ValueError(
                f"The [{self.config_file_path}].{self.compilation_mode.value}.compilation_tool {compilation_tool} is not SafeCompilationTool!"
            )

        self.compilation_tool = (
            FastCompilationToolTypes(compilation_tool)
            if self.compilation_mode == CompilationModeTypes.FAST
            else SafeCompilationToolTypes(compilation_tool)
        )

        self.compilation_tool_config = self.compilation_mode_config.get(
            self.compilation_tool.value
        )

    def parse(self):
        self.parse_config_file()

    def __str__(self):
        return f"<Factory Version {self.version_name} in {self.compilation_mode} mode with {self.compilation_tool} tool>"
