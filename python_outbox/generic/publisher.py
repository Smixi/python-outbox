import requests
from cloudevents.conversion import to_structured
from cloudevents.pydantic import CloudEvent

from ..base.publisher import AbstractPublisher, PublishFailedException


class CloudEventHTTPPublisher(AbstractPublisher):
    """Post the data as a cloud event."""

    def __init__(self, url, session: None | requests.Session = None):
        self.url = url
        self.session: requests.Session = (
            session if session is not None else requests.Session()
        )
        super().__init__()

    def publish(self, item: dict) -> None:
        """Publish the cloud event to the given url. The item must conform to the cloud event minimal requirements (type, source)"""
        try:
            cloud_event = CloudEvent(**item)
            headers, data = to_structured(cloud_event)
            response: requests.Response = self.session.post(
                self.url, data=data, headers=headers
            )
        except Exception as exc:
            raise PublishFailedException(
                f"Cannot publish cloudevent to {self.url}"
            ) from exc

        if response.status_code != 200:
            raise PublishFailedException(
                f"Cloud event published failed, server responded with a status != 200 OK. Server returned {response.status_code}"
            )
