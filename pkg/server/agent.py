from pkg.metrics.prometheus import (
    EVENTS_INGESTED,
    EVENTS_PROCESSED,
    ALERT_COUNT,
)
from typing import List, Any
import faust


def RegisterAgent(app: faust.App, topicName: str, rules: List[Any]):
    """
    This function will register a Faust Agent to
    consume events from the defined topic.
    Additionally, this function will also register
    the rules associated with this topic with
    corresponding metrics


    Parameters:
        topicName (str): Name of message topic that messages are being consumed from
        rules (List[Any]): List of loaded modules which reference the rule
    """

    @app.agent(topicName, name=f"{topicName}-agent")
    async def match(stream: Any):
        """Produce streams of transformed data"""
        async for event in stream:
            EVENTS_INGESTED.labels(topicName).inc()
            for mod_rule in rules:
                if mod_rule.rule(event=event):
                    print(event)
                    ALERT_COUNT.labels(topicName, mod_rule.__name__).inc()
                EVENTS_PROCESSED.labels(topicName, mod_rule.__name__).inc()
