import logging


class Logger:
    def __init__(self, system):
        if not system:
            raise Exception(f"The system {system} cannot be empty!")
        self.system = system

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("jetcert")

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
