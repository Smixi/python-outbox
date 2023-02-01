# Python-Outbox

Python-outbox is a library that implement the Outbox pattern.

It try to separate concerns of retrieving and publishing events in the pattern, allowing a generic implementation for any use case you would want.

# The Outbox Pattern

The outbox pattern is used to solve the problem of sending event and updating a database during a transaction. To do that, we save the event information in the same transaction and a runner will handle publishing the event. More information can be found on [Microservices.io](https://microservices.io/patterns/data/transactional-outbox.html).

# How to use this library

## Installation

Note: This is a beta project and things might breaks.

```bash
pip install python-outbox
```

## Concepts

This library tries use the fact outbox pattern is based on the following operations:

* The event is created and saved in the database
* A separate process runs
* This process fetch events regularly
* The process tries to push those events to a consumer (a broker, an API, etc)

In order to make those operation generics and allows to change the way you want to handle publishing and retrieving events, we define those specifics class:

* StorageBox: The entity that is stored an contains the events and events metadata
* Source: The source role is to fetch the storage box entities.
* Publisher: The Publisher class will publish specific items to a consumer.
* Mapper: A mapper map a fetch item from a Source instance to a publishable type
* Producer: A producer knows how link a source, publisher and mapper altogether
* Runner: A runner will regularly run the producer steps to fetch and publish events.

## Example:

Code example incoming. An example using this library is available here at this time: https://github.com/Smixi/knative_journey

# Documentation:

Incomming.

## TODO

* Documentation
* Examples
* More implementation of Runner, Mapper and Publisher to support Celery/Redis, etc.

