from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import TypedDict, Dict
import logging


@dataclass
class Meta:
    name: str
    version: str
    description: str
    author: str


class OutputInterface(metaclass=ABCMeta):
    """Interface for output plugins"""

    meta: Meta

    def __init__(self, logger: logging.Logger) -> None:
        """
        Entry init block for plugins
        params:
            logger (Logger): logger for logging
        """
        self.logger = logger

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin"""

    @abstractmethod
    def run(self, event: TypedDict, ruleMetdata: Dict[str, TypedDict]) -> None:
        """Run the plugin"""
