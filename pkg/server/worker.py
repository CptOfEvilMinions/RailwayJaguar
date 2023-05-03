from pkg.metrics.prometheus import (
    GenerateTopicAlert,
    EVENTS_INGESTED,
    EVENTS_PROCESSED,
    ALERT_COUNT
)
from typing import List, Any, Dict
import faust

def RegisterWorker(app: faust.App, topic: str, rules: List[Any]):
    """
    First this function will create a metric counter
    for the message topic. Next, a Faust worker is
    registered to consume events from the defined 
    message topic.

    Parameters:
        topic (str): Name of message topic that messages are being consumed from
        rules (List[Any]): List of loaded modules which reference the rule
    """
    metric_alert_counter = GenerateTopicAlert(topic)

    @app.agent(topic)
    async def match(stream: List[Dict[str, Any]]):
        async for event in stream:
            ##EVENTS_INGESTED.inc()
            async  for mod_rule in rules:
                if mod_rule.rule(event=event):
                    ##EVENTS_PROCESSED.inc()
                    with open("alerts.txt", "a")as f:
                        f.write(str(event) + "\n")
                    print(event)
                    ##ALERT_COUNT.inc()
                    ##metric_alert_counter.inc()
                ##else:
                    ##EVENTS_PROCESSED.inc()
