from sqlalchemy.orm import Session

from python_outbox.generic.publisher import VoidPublisher
from python_outbox.sqlalchemy_outbox.sqlalchemy_mapper import \
    SQLAlchemyStorageBoxMapper
from python_outbox.sqlalchemy_outbox.sqlalchemy_producer import \
    SQLAlchemyStorageBoxProducer
from python_outbox.sqlalchemy_outbox.sqlalchemy_source import \
    SQLAlchemyStorageBoxSource
from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import \
    SQLAlchemyPydanticStorageBox


def test_sqlalchemy_storage_box_producer(dbsession: Session):
    with dbsession:
        source = SQLAlchemyStorageBoxSource(dbsession)
        mapper = SQLAlchemyStorageBoxMapper()
        publisher = VoidPublisher()
        producer = SQLAlchemyStorageBoxProducer(
            source=source, mapper=mapper, publisher=publisher
        )
        first_run = producer.produce()

        assert first_run == 0

        item = SQLAlchemyPydanticStorageBox(payload={"key": "value"})
        dbsession.add(item)
        dbsession.commit()
        second_run = producer.produce()
        assert second_run == 1

        third_run = producer.produce()

        assert third_run == 0
