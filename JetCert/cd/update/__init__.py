class Update:
    def __init__(self, version):
        self.version = version
        self.created_at = time.time()

    def get_version(self):
        return self.version

    def get_created_at(self):
        return self.get_created_at

    def get_id(self):
        return self.version.get_version_name()

    def get_utility(self):
        compiles_number = self.version.get_compiles_number()
        requests_number = self.version.get_requests_number()
        return compiles_number - requests_number

    def build(self):
        self.version.compile()

    def __lt__(self, other):
        return self.get_utility() < other.get_utility()

    def __str__(self):
        version_name = self.version.get_version_name()
        module_name = self.version.get_module_name()
        return f"<Update in {version_name} from {module_name}>"
