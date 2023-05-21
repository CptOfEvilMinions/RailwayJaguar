from confluent_kafka import Producer
import argparse
import glob
import json
import os.path


def json_serializer(msg: str):
    return json.dumps(json.loads(msg)).encode("utf-8")


def init_kafka_connector(args: argparse.ArgumentParser):
    conf = {
        "bootstrap.servers": f"{args.bootstrapServers}",
    }
    return Producer(conf)


def main(args: argparse.ArgumentParser):
    producer = init_kafka_connector(args)
    producer.poll(0)
    for logFile in glob.glob(os.path.expanduser(args.logFilesGlob)):
        with open(logFile, "r", encoding="utf-8") as f:
            print(logFile)
            for line in f:
                producer.produce(
                    topic=f"{args.logSource}_{args.logType}",
                    value=json_serializer(line),
                )
                producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSONSerailizer example")
    parser.add_argument(
        "-b",
        dest="bootstrapServers",
        required=True,
        help="Bootstrap broker(s) (host[:port])",
    )
    parser.add_argument(
        "--logFilesGlob",
        dest="logFilesGlob",
        default="logs/*.log",
        required=True,
        help="Filter for log files",
    )
    parser.add_argument(
        "--logSource",
        dest="logSource",
        required=True,
        help="Log type",
    )
    parser.add_argument(
        "--logType",
        dest="logType",
        required=True,
        help="Log type",
    )

    main(parser.parse_args())
