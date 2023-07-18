from pkg.outputs.model import OutputInterface, Meta
from jira import JIRA, Issue
from typing import Any, Dict
from logging import Logger
import os


class Plugin(OutputInterface):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.meta = Meta(
            name="jira",
            version="0.0.1",
            description="Create JIRA ticket from alert",
            author="CptOfEvilMinions",
        )
        self.url: str
        self.project: str
        self.email: str
        self.token: str

    def initialize(self) -> None:
        self.url = os.environ["JIRA_API_URL"]
        self.project = os.environ["JIRA_PROJECT"]
        self.email = os.environ["JIRA_EMAIL"]
        self.token = os.environ["JIRA_TOKEN"]
        self.client = JIRA(basic_auth=(self.email, self.token), server=self.url)

    def run(self, event: Any) -> None:
        msg = f"""
        {event}
        """
        issue_dict: Dict[str, Dict[str, str] | str] = {
            "project": {"key": self.project},
            "summary": "Testing issue from Python Jira Handbook",
            "description": msg,
            "issuetype": {"name": "Bug"},
        }
        new_issue: Issue = self.client.create_issue(fields=issue_dict)
        self.logger.info(new_issue)
