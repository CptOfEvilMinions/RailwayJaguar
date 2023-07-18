from pkg.outputs.model import OutputInterface, Meta
from slack_sdk.webhook import WebhookClient
from logging import Logger
from typing import Any
import os


class Plugin(OutputInterface):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.meta = Meta(
            name="slack",
            version="0.0.1",
            description="Send alerts to Slack channel",
            author="CptOfEvilMinions",
        )
        self.webhook: str
        self.client: WebhookClient

    def initialize(self) -> None:
        self.webhook = os.environ["SLACK_WEBHOOK"]
        self.client = WebhookClient(self.webhook)

    def run(self, event: Any) -> None:
        msg = f"""
        :rotating-light-red: :rotating-light-red: :rotating-light-red:
        {event}
        """
        response = self.client.send(text=msg)
        if response.status_code != 200:
            self.logger.error("[-] - Unable to send Slack message")
