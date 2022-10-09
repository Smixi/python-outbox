import importlib
import json
from datetime import datetime
from enum import Enum
from uuid import uuid4

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy_utils import JSONType, UUIDType

from ..base.storage_box import StorageBoxMixin
from ..base.type import PayloadT
from .sqlalchemy_base import Base


class SQLAlchemyStorageBoxMixin(StorageBoxMixin[PayloadT], Base):
    """
    An SQL StorageBox mixin to hold any serializable type
    When using SQLAlchemy, you must use this serializer with the json_serializer:
    create_engine("...", json_serializer=SQLAlchemyStorageBoxMixin.serializer)
    Or use a custom serializer. It allows to serialize/deserialize Pydantic nicely while keeping JSON object support for
    postgres.
    """

    class StatusEnum(Enum):
        FAILED = "Failed"
        PUBLISHED = "Published"
        WAITING = "Waiting"

    __tablename__ = "sqlalchemy_storagebox"

    __abstract__: True

    id = sa.Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    _payload = sa.Column("payload", JSONType)
    status = sa.Column(sa.Enum(StatusEnum), default=StatusEnum.WAITING)
    retries = sa.Column(sa.Integer, default=0)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    @classmethod
    def serializer(cls, item: object):
        if issubclass(item.__class__, BaseModel):
            return item.json()
        return json.dumps(item)


class SQLAlchemyPydanticStorageBox(SQLAlchemyStorageBoxMixin):
    """An SQL StorageBox to hold any Pydantic serializable type"""

    class_name = sa.Column(sa.String)
    module_name = sa.Column(sa.String)

    def __init__(self, payload=None):
        self.payload = payload
        super().__init__()

    @property
    def payload(self) -> BaseModel:
        return self.pull()

    @payload.setter
    def payload(self, item: BaseModel):
        self.put(item)

    def pull(self) -> BaseModel:
        # When the object is not already saved in DB and is still a Pydantic object
        if issubclass(self._payload.__class__, BaseModel):
            return self._payload
        module = importlib.import_module(self.module_name)
        klass: BaseModel = getattr(module, self.class_name)
        return klass(**self._payload)

    def put(self, item: BaseModel) -> None:
        self._payload = item
        item_class = item.__class__
        self.module_name = item_class.__module__
        self.class_name = item_class.__name__


class SQLAlchemyJsonStorageBox(SQLAlchemyStorageBoxMixin):
    """An SQL StorageBox to hold any JSON value. The holded item MUST be json serializable (only dict with litterals)."""

    def __init__(self, payload=None):
        self.payload = payload
        super().__init__()

    @property
    def payload(self) -> BaseModel:
        return self.pull()

    @payload.setter
    def payload(self, item: BaseModel):
        self.put(item)

    def pull(self) -> BaseModel:
        return self._payload

    def put(self, item: BaseModel) -> None:
        self._payload = item
