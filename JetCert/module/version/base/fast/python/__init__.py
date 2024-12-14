from builder import Builder
from module.version.base.fast import FastVersion
from module.version.base.fast import FastCompilationToolTypes


class PythonVersion(FastVersion):
    def __init__(
        self,
        module,
        version_name,
        compilation_mode_config,
        compilation_tool_config,
    ):
        super().__init__(module, version_name, compilation_mode_config)

        self.compilation_tool = FastCompilationToolTypes.PYTHON

    def get_compilation_tool(self):
        return self.compilation_tool

    def run(self, inputs=None):
        super().run()

        entry_file_path = self.get_entry_file_path()
        response = Builder.run_python_file(entry_file_path, inputs=inputs)
        return super().sign(response)

    def __str__(self):
        return f"<Python Version {self.version_name}>"
