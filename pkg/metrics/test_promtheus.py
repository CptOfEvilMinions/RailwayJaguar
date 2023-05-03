from pkg.metrics.prometheus import GenerateTopicAlert
from prometheus_client import Counter

def test_GenerateTopicAlert():
    topic_name = "test"
    c = GenerateTopicAlert(topic_name)

    assert isinstance(c, Counter)
    assert c._name == f"{topic_name}_alerts"