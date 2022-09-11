from pydantic import BaseModel
from sqlalchemy.orm import Session

from python_outbox.sqlalchemy_outbox.sqlalchemy_mapper import \
    SQLAlchemyStorageBoxMapper
from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import \
    SQLAlchemyPydanticStorageBox


class APydanticClass(BaseModel):
    test_value: str


def test_sql_alchemy_mapper():
    test_value = "test_this_payload"
    outbox_item = SQLAlchemyPydanticStorageBox()
    outbox_item.payload = APydanticClass(test_value=test_value)
    mapper = SQLAlchemyStorageBoxMapper()
    mapped = mapper.convert(outbox_item)
    assert mapped == outbox_item.payload
