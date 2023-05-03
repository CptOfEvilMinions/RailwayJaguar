from prometheus_client import Counter

EVENTS_INGESTED = Counter(
    "events_ingested",
    "Count of how many events have been ingested",
)

EVENTS_PROCESSED = Counter(
    "events_processed",
    "Count of how many events have been ingested",
)

ALERT_COUNT = Counter(
    "alerts",
    "Count of how many events triggered alerts",
)

def GenerateTopicAlert(topic: str) -> Counter:
    """
    Returns a metric counter for an message topic

    Parameters:
        topic (str): Name of topic for alert counter
    
    Return
        (Counter): Prometheus metric counter 
    """
    return Counter(
        f"{topic}_alerts",
        "Count of how many events triggered alerts",
    )