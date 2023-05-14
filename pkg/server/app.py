from typing import List
import faust
import yarl


def RegisterFaustApp(app_name: str, kafka_brokers: List[str]) -> faust.App:
    """
    Register a Faust app

    Parameters:
        app_name (str): App name
        kafka_brokers (List[str]): List of Kafka broker servers

    Return
        (faust.App) - Faust app to register workers
    """
    # https://github.com/robinhood/faust/issues/156
    return faust.App(
        app_name,
        broker=[f"kafka://{yarl.URL(kb)}" for kb in kafka_brokers],
    )
