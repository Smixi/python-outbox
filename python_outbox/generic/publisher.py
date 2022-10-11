from typing import Any

import requests
from cloudevents.conversion import to_structured
from cloudevents.pydantic import CloudEvent

from ..base.publisher import AbstractPublisher, PublishFailedException


class CloudEventHTTPPublisher(AbstractPublisher[CloudEvent]):
    """Post the data as a cloud event."""

    def __init__(self, url, session: None | requests.Session = None):
        self.url = url
        self.session: requests.Session = (
            session if session is not None else requests.Session()
        )
        super().__init__()

    def publish(self, cloud_event: CloudEvent) -> None:
        """
        Publish the cloud event to the given url.
        """
        try:
            headers, data = to_structured(cloud_event)
            response: requests.Response = self.session.post(
                self.url, data=data, headers=headers
            )
        except Exception as exc:
            raise PublishFailedException(
                f"Cannot publish cloudevent to {self.url}"
            ) from exc

        if response.status_code < 200 or response.status_code >= 300:
            raise PublishFailedException(
                "Cloud event published failed, server responded with a status != 200"
                f" OK. Server returned {response.status_code}"
            )


class VoidPublisher(AbstractPublisher[Any]):
    """A publisher that consume anything but publish nothing"""

    def publish(self, item: Any) -> None:
        return
