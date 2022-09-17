from time import sleep

from python_outbox.base.producer import AbstractProducer
from python_outbox.generic.runner import SimpleRunner


def test_simple_runner():
    class TestProducer(AbstractProducer):
        def __init__(self) -> None:
            self.count = 0
            super().__init__(None, None, None)

        def produce(self) -> int:
            self.count += 1
            return self.count

    producer = TestProducer()
    runner = SimpleRunner(producer=producer, wait_seconds=1e-3)

    # Here we should mock the run function to be synchronous and immediatly stop the function.
    runner.start()
    sleep(5e-3)
    runner.stop()

    assert producer.count != 0
