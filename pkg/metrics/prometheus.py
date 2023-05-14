from prometheus_client import Counter

EVENTS_INGESTED = Counter(
    "events_ingested", "Count of how many events have been ingested", ["topic"]
)

EVENTS_PROCESSED = Counter(
    "events_processed", "Count of how many events have been ingested", ["topic", "rule"]
)

ALERT_COUNT = Counter(
    "alerts", "Count of how many events triggered alerts", ["topic", "rule"]
)
