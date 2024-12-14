from utils import Utils
from builder import Builder
from module.version.base.fast import FastVersion
from module.version.base.fast import FastCompilationToolTypes


class CodonVersion(FastVersion):
    def __init__(
        self,
        module,
        version_name,
        compilation_mode_config,
        compilation_tool_config,
    ):
        super().__init__(module, version_name, compilation_mode_config)

        self.compilation_tool = FastCompilationToolTypes.CODON

    def get_compilation_tool(self):
        return self.compilation_tool

    def compile(self):
        super().compile()

        entry_file_path = self.get_entry_file_path()
        response = Builder.compile_codon_file(entry_file_path)
        is_compile_invalid = response.get("process").get("returncode")
        if is_compile_invalid:
            raise ValueError(f"The is_compile {is_compile_invalid} is not valid!")

    def run(self, inputs=None):
        super().run()

        entry_file_path = self.get_entry_file_path()
        entry_base_file_path = Utils.get_base_file_path(entry_file_path)
        response = Builder.run_exe_file(entry_base_file_path, inputs=inputs)
        return super().sign(response)

    def __str__(self):
        return f"<Codon Version {self.version_name}>"
