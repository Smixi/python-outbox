import logging
from datetime import datetime

from python_outbox.sqlalchemy_outbox.sqlalchemy_mapper import SQLAlchemyStorageBoxMapper
from python_outbox.sqlalchemy_outbox.sqlalchemy_source import SQLAlchemyStorageBoxSource

from ..base.producer import AbstractProducer
from ..base.publisher import AbstractPublisher
from ..base.type import PayloadT
from .sqlalchemy_storage_box import SQLAlchemyStorageBoxMixin


class SQLAlchemyStorageBoxProducer(
    AbstractProducer[SQLAlchemyStorageBoxSource[PayloadT], PayloadT]
):
    def __init__(
        self,
        source: SQLAlchemyStorageBoxSource[PayloadT],
        mapper: SQLAlchemyStorageBoxMapper[PayloadT],
        publisher: AbstractPublisher[PayloadT],
    ):
        self.source = source
        self.mapper = mapper
        self.publisher = publisher

    def produce(self) -> int:
        items = self.source.fetch_items()
        produced = 0
        for item in items:
            try:
                mapped = self.mapper.convert(item)
                self.publisher.publish(mapped)
                item.status = SQLAlchemyStorageBoxMixin.StatusEnum.PUBLISHED
                produced += 1
            except Exception as exc:
                item.retries = item.retries + 1
                # Set to failed after certain amount of retries.
                # item.status = SQLAlchemyStorageBoxMixin.StatusEnum.FAILED
                logging.exception(exc)
            item.updated_at = datetime.utcnow()
            self.source.session.add(item)
        self.source.session.commit()
        return produced
