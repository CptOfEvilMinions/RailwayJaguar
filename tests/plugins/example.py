from pkg.outputs.model import OutputInterface, Meta
from logging import Logger
from typing import Any


class Plugin(OutputInterface):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.meta = Meta(
            name="example",
            version="0.0.1",
            description="Example plugin for testing",
            author="CptOfEvilMinions",
        )

    def initialize(self) -> None:
        return

    def run(self, event: Any) -> None:
        msg = f"""
        :rotating-light-red: :rotating-light-red: :rotating-light-red:
        {event}
        """
        print(msg)
