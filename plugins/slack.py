from pkg.outputs.model import OutputInterface, Meta
from slack_sdk.webhook import WebhookClient
from logging import Logger
from typing import TypedDict


class Plugin(OutputInterface):
    """
    Slack plugin that sends an alert to
    a designated channel using webhook
    """

    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.meta = Meta(
            name="slack",
            version="0.0.1",
            description="Send alerts to Slack channel",
            author="CptOfEvilMinions",
        )
        self.client: WebhookClient

    def initialize(self) -> None:
        """
        Initialize Slack client
        """
        _token: str = open("/run/secrets/railwayjaguar-slack-token", "r").read().strip()
        self.client = WebhookClient(_token)

    def run(self, event: TypedDict) -> None:
        """
        Post a Slack message using Slack client

        Params:
            event (TypedDict): Alert JSON payload

        """
        msg = f"""
        :rotating-light-red: :rotating-light-red: :rotating-light-red:
        {event}
        """
        response = self.client.send(text=msg)
        if response.status_code != 200:
            self.logger.error("[-] - Unable to send Slack message")
