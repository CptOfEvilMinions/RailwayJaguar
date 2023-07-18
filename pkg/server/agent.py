from pkg.metrics.prometheus import (
    EVENTS_INGESTED,
    EVENTS_PROCESSED,
    ALERT_COUNT,
)
from pkg.rules.model import Rule
from typing import List, Any, Dict
from types import ModuleType
import faust


def RegisterAgent(
    app: faust.App,
    topicName: str,
    rules: List[Rule],
    outputPlugins: Dict[str, ModuleType],
):
    """
    This function will register a Faust Agent to
    consume events from the defined topic.
    Additionally, this function will also register
    the rules associated with this topic with
    corresponding metrics


    Parameters:
        app (faust.App): Used to register a new agent
        topicName (str): Name of message topic that messages are being consumed from
        rules (List[Any]): List of loaded modules which reference the rule
        outputPlugins
    """

    @app.agent(topicName, name=f"{topicName}-agent")
    async def match(stream: Any):
        """Produce streams of transformed data"""
        async for event in stream:
            EVENTS_INGESTED.labels(topicName).inc()
            for rule in rules:
                if rule.run(event=event):
                    # Send event to output
                    for output in rule.Metadata.Outputs:
                        outputPlugins[output].run(event)
                    ALERT_COUNT.labels(topicName, rule.Metadata.Metadata["name"]).inc()
                EVENTS_PROCESSED.labels(topicName, rule.Metadata.Metadata["name"]).inc()
