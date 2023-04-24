# RailwayJaguar
A Pytohn rule based detection platform for Kafka

## Local dev
### Spin up Docker kafka instance
1. `brew install kcat`
1. `docker-compose up -d`
1. `kcat -P -b localhost:9092 -t zeek_conn`
1. List Kafka topics: `kcat -L -b localhost:9092`
1. Consume 5 messages: `kcat -C -b localhost:9092 -t zeek_conn -c 5`

## References
* [Python | Interconversion between Dictionary and Bytes](https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/)
* [confluentinc/cp-zookeeper](https://hub.docker.com/r/confluentinc/cp-zookeeper/tags?page=1&name=7.3)
* [cp-all-in-one/cp-all-in-one-community/docker-compose.yml](https://github.com/confluentinc/cp-all-in-one/blob/7.3.0-post/cp-all-in-one-community/docker-compose.yml)
* [Quick Start for Confluent Platform](https://docs.confluent.io/platform/current/platform-quickstart.html#quick-start-for-cp)
* [Learn how to use Kafkacat – the most versatile Kafka CLI client](https://codingharbour.com/apache-kafka/learn-how-to-use-kafkacat-the-most-versatile-cli-client/)
* [Learn how to use Kafkacat – the most versatile Kafka CLI client](https://dev.to/de_maric/learn-how-to-use-kafkacat-the-most-versatile-kafka-cli-client-1kb4)
* [Convert dictionary to bytes and back again python? [duplicate]](https://stackoverflow.com/questions/19232011/convert-dictionary-to-bytes-and-back-again-python)
* [confluent-kafka-python/examples/json_producer.py](https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/json_producer.py)
* [Loading and parsing a JSON file with multiple JSON objects](https://stackoverflow.com/questions/12451431/loading-and-parsing-a-json-file-with-multiple-json-objects)
* [Read Json file and post to Kafka topic](https://copyprogramming.com/howto/read-json-file-and-post-to-kafka-topic)
* [A Python Script Template with Sub-commands (and Type Hints)](https://adamj.eu/tech/2021/10/15/a-python-script-template-with-sub-commands-and-type-hints/)
* [Python example of using argparse sub-parser, sub-commands and sub-sub-commands](https://gist.github.com/jirihnidek/3f5d36636198e852280f619847d22d9e)
* [Pytest Tutorial – How To Use Pytest For Python Testing](https://www.softwaretestinghelp.com/pytest-tutorial/)
* [What's the canonical way to check for type in Python?](https://stackoverflow.com/questions/152580/whats-the-canonical-way-to-check-for-type-in-python)
* [Build Command-Line Interfaces With Python's argparse](https://realpython.com/command-line-interfaces-python-argparse/)
* [faust-streaming/faust](https://github.com/faust-streaming/faust)
* []()
* []()
* []()
* []()
* []()
* []()