import logging

import yaml
from kubernetes import client

from .model import Event

log = logging.getLogger('event')


def get_namespace_events(namespace_name):
    v1core = client.CoreV1Api()
    _events = v1core.list_namespaced_event(namespace_name)
    log.debug(yaml.dump(_events))
    return _events


def generate_my_event(_event):
    log.debug(yaml.dump(_event))
    return Event(
        _event.count,
        _event.message,
        _event.last_timestamp,
        _event.reason,
        _event.type,
        _event.involved_object.kind,
        _event.involved_object.name
    )


def get_my_events(_namespace_name):
    return [generate_my_event(e) for e in get_namespace_events(_namespace_name).items]
