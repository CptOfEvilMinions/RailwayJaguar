from confluent_kafka import Consumer
from typing import Dict, Union

def InitConsumer(conf) -> Consumer:
    c: Dict[str, Union[str,int]] = {
        "bootstrap.servers": "host1:9092,host2:9092",
        "group.id": "foo",
        "auto.offset.reset": "smallest"
    }
    return Consumer(c)
 