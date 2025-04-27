from utils import Utils
from builder import Builder
from module.version.base.safe import SafeVersion
from module.version.base.safe import SafeCompilationToolTypes


class CompCertVersion(SafeVersion):
    def __init__(
        self,
        module,
        version_name,
        compilation_mode_config,
        compilation_tool_config,
    ):
        super().__init__(module, version_name, compilation_mode_config)

        if not compilation_tool_config:
            raise Exception(
                f"The compilation_tool config {compilation_tool_config} cannot be empty!"
            )

        self.compilation_tool = SafeCompilationToolTypes.COMPCERT
        self.linked_files = []

        linked_files = compilation_tool_config.get("linked_files")
        if linked_files:
            if type(linked_files) != list:
                raise Exception(f"The linked_files {linked_files} is not list!")
            self.linked_files = linked_files

    def get_compilation_tool(self):
        return self.compilation_tool

    def get_linked_files(self):
        return self.linked_files

    def compile(self):
        super().compile()

        entry_file_path = self.get_entry_file_path()
        response = Builder.compile_compcert_file(
            entry_file_path,
            linked_files=self.linked_files,
        )
        is_compile_invalid = response.get("process").get("returncode")
        if is_compile_invalid:
            raise Exception(f"The is_compile {is_compile_invalid} is not valid!")

    def run(self, inputs=None):
        super().run()

        entry_file_path = self.get_entry_file_path()
        entry_base_file_path = Utils.get_base_file_path(entry_file_path)
        response = Builder.run_exe_file(entry_base_file_path, inputs=inputs)
        return super().sign(response)

    def __str__(self):
        return f"<CompCert Version {self.version_name}>"
