from utils import Utils
from builder import Builder
from module.version.base.fast import FastVersion
from module.version.base.fast import FastCompilationToolTypes


class NumbaVersion(FastVersion):
    def __init__(
        self,
        module,
        version_name,
        compilation_mode_config,
        compilation_tool_config,
    ):
        super().__init__(module, version_name, compilation_mode_config)

        if not compilation_tool_config:
            raise ValueError(
                f"The compilation_tool config {compilation_tool_config} cannot be empty!"
            )

        self.compilation_tool = FastCompilationToolTypes.NUMBA
        self.entry_func_name = "go_fast"
        self.cache_function = None

        entry_func_name = compilation_tool_config.get("entry_func_name")
        if entry_func_name:
            if not Utils.is_valid_python_func_name(entry_func_name):
                raise ValueError(
                    f"The entry_func_name {entry_func_name} is not the name of a python function!"
                )
            self.entry_func_name = entry_func_name

    def get_compilation_tool(self):
        return self.compilation_tool

    def get_entry_func_name(self):
        return self.entry_func_name

    def compile(self):
        super().compile()

        entry_file_path = self.get_entry_file_path()
        response = Builder.compile_numba_file(
            entry_file_path,
            entry_func_name=self.entry_func_name,
        )
        is_compile_invalid = response.get("process").get("returncode")
        if is_compile_invalid:
            raise ValueError(f"The is_compile {is_compile_invalid} is not valid!")

        self.cache_function = response.get("result")

    def run(self, inputs=None):
        super().run()

        response = Builder.run_numba_func(self.cache_function, inputs=inputs)
        return super().sign(response)

    def __str__(self):
        return f"<Numba Version {self.version_name}>"
