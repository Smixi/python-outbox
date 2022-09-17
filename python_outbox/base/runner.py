from abc import ABC

from .producer import AbstractProducer


class Runner(ABC):
    """A runner call once started tries to regularly call the producer to produce events, if any."""

    def __init__(self, producer: AbstractProducer):
        self.producer = producer

    def start() -> None:
        pass

    def stop() -> None:
        pass
