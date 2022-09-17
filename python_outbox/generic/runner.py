from multiprocessing.resource_sharer import stop
from threading import Thread
from time import sleep

from python_outbox.base.producer import AbstractProducer

from ..base.runner import Runner


class SimpleRunner(Runner):
    """The SimpleRunner is simply a loop trying to produce the events in another thread, then sleeping every X seconds, repeats until stopped"""

    def __init__(self, producer: AbstractProducer, wait_seconds=1):
        self.wait_seconds = wait_seconds
        self.stop_loop = False
        self.thread_loop = None
        super().__init__(producer)

    def start(self) -> None:
        self.stop_loop = False
        self._run()

    def stop(self) -> None:
        self.stop_loop = True

    def _run(self) -> None:
        """Create the thread loop and start it"""
        self.thread_loop = Thread(target=self.loop)
        self.thread_loop.start()

    def loop(self) -> None:
        while self.stop_loop is not True:
            self.producer.produce()
            sleep(self.wait_seconds)
