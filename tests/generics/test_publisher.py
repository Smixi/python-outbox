import pytest
import requests
import responses
from cloudevents.http import CloudEvent as HttpCE
from cloudevents.http import from_http
from cloudevents.pydantic import CloudEvent
from deepdiff import DeepDiff

from python_outbox.generic.publisher import (CloudEventHTTPPublisher,
                                             PublishFailedException,
                                             VoidPublisher)


@responses.activate
def test_http_cloud_event_publisher():
    url = "https://test/ce/publisher"

    cloud_event_data = {
        "source": "source_test",
        "type": "source_type",
        "test_field": "test_field_value",
    }
    cloud_event = CloudEvent(**cloud_event_data)
    cloud_event_dict = cloud_event.dict()

    def check_ce(request: requests.PreparedRequest):
        parsed_ce = from_http(data=request.body, headers=request.headers)
        return (
            not DeepDiff(
                parsed_ce.data,
                cloud_event_dict,
                ignore_order=True,
                exclude_types=[HttpCE, dict],
            ),
            "Cloud event doesn't match",
        )

    responses.post(status=200, url=url, match=[check_ce])

    publisher = CloudEventHTTPPublisher(url=url)
    publisher.publish(cloud_event.dict())

    # Check with raw dict:
    responses.post(status=200, url=url, match=[check_ce])
    publisher.publish(cloud_event_data)

    # Request return other than a 404
    responses.post(status=404, url=url, match=[check_ce])
    with pytest.raises(PublishFailedException):
        publisher.publish(cloud_event_dict)

    # Connection error, no host
    with pytest.raises(PublishFailedException):
        publisher.publish(cloud_event_dict)


def test_void_publisher():
    publisher = VoidPublisher()
    publisher.publish({})
