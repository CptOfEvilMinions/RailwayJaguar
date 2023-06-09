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
    # internal: bool - If set to True this means we own and are
    # responsible for this topic: we are allowed to create or
    # delete the topic.
    sinkTopic = app.topic(f"{topicName}-alerts", internal=True)

    @app.agent(topicName, name=f"{topicName}-agent", sink=[sinkTopic])
    async def match(stream: Any):
        """Produce streams of transformed data"""
        async for event in stream:
            EVENTS_INGESTED.labels(topicName).inc()
            for mod_rule in rules:
                if mod_rule.rule(event=event):
                    yield event
                    ALERT_COUNT.labels(topicName, mod_rule.__name__).inc()
                EVENTS_PROCESSED.labels(topicName, mod_rule.__name__).inc()
