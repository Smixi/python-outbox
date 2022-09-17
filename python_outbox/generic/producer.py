from ..base.producer import AbstractProducer


class VoidProducer(AbstractProducer):
    """A producer that does nothing"""

    def produce(self) -> int:
        return 0
