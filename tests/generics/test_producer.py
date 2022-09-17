from python_outbox.generic.producer import VoidProducer


def test_void_producer():
    producer = VoidProducer(None, None, None)
    assert producer.produce() == 0
