import pytest
from cloudevents.pydantic import CloudEvent
from pydantic import BaseModel
from sqlalchemy.orm import Session

from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import (
    SQLAlchemyJsonStorageBox, SQLAlchemyPydanticStorageBox)


class APydanticModel(BaseModel):
    test_field: str


def test_fixture_db_works(dbsession):
    pass


def test_pull_put_pydantic_sqlalchemy_storage_box(dbsession: Session):
    with dbsession:
        test_value = "test_this_payload"
        outbox_item = SQLAlchemyPydanticStorageBox()
        payload_item = APydanticModel(test_field=test_value)
        outbox_item.payload = payload_item
        dbsession.add(outbox_item)
        dbsession.commit()
        outbox_item_fetched: SQLAlchemyPydanticStorageBox = dbsession.query(
            SQLAlchemyPydanticStorageBox
        ).first()
        payload: APydanticModel = outbox_item_fetched.payload
        assert payload.test_field == test_value


def test_pull_put_cloudevent_sqlalchemy_storage_box(dbsession: Session):
    with dbsession:
        test_value = "test_this_payload"
        ce_source = "test"
        ce_type = "ce_type"
        outbox_item = SQLAlchemyPydanticStorageBox()
        payload_item = CloudEvent(test_field=test_value, source=ce_source, type=ce_type)
        outbox_item.payload = payload_item
        dbsession.add(outbox_item)
        dbsession.commit()
        outbox_item_fetched: SQLAlchemyPydanticStorageBox = dbsession.query(
            SQLAlchemyPydanticStorageBox
        ).first()
        payload: CloudEvent = outbox_item_fetched.payload
        assert payload.get("test_field") == test_value


def test_pull_put_json_sqlalchemy_storage_box(dbsession: Session):
    with dbsession:
        test_value = "test_this_payload"
        outbox_item = SQLAlchemyJsonStorageBox()
        payload_item = {"value": test_value}
        outbox_item.payload = payload_item
        dbsession.add(outbox_item)
        dbsession.commit()
        outbox_item_fetched: SQLAlchemyJsonStorageBox = dbsession.query(
            SQLAlchemyJsonStorageBox
        ).first()
        payload: APydanticModel = outbox_item_fetched.payload
        assert payload["value"] == test_value
