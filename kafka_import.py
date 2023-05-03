from confluent_kafka import Producer
from uuid import uuid4
import argparse
import glob
import json


def json_serializer(msg: str):
    return json.dumps(json.loads(msg)).encode("utf-8")


def init_kafka_connector(args):
    conf = {
        "bootstrap.servers": f"{args.bootstrap_servers}",
    }
    return Producer(conf)


def main(args):
    producer = init_kafka_connector(args)
    producer.poll(0)
    #for zeek_log_file in glob.glob("logs/sysmon*.log"):
    #    zeek_type = "sysmon"
    for zeek_log_file in glob.glob(f"logs/{args.log_filter}.log"):
        zeek_type = zeek_log_file.split("/")[1].split(".")[0]
        with open(zeek_log_file, "r", encoding="utf-8") as f:
            print(zeek_log_file)
            for line in f:
                producer.produce(
                    topic=f"zeek_{zeek_type}",
                    value=json_serializer(line),
                )
                producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSONSerailizer example")
    parser.add_argument(
        "-b",
        dest="bootstrap_servers",
        required=True,
        help="Bootstrap broker(s) (host[:port])",
    )
    parser.add_argument(
        "--log_filter",
        dest="log_filter",
        default="*",
        required=False,
        help="Filter for log files",
    )

    main(parser.parse_args())
