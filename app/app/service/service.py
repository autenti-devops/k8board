import logging

import yaml
from kubernetes import client

from .model import Service, ServicePort
from ..pod.service import get_service_pods, generate_my_pod

log = logging.getLogger('service')


def generate_my_service(service_, pods_):
    if pods_ is None:
        pods_ = [generate_my_pod(p) for p in get_service_pods(service_)]
    _service = Service(
        service_.metadata.name,
        [ServicePort(sp.name, sp.port, sp.protocol, sp.target_port) for sp in service_.spec.ports or []],
        service_.spec.selector,
        service_.metadata.labels,
        pods_
    )
    log.debug("=== generate_my_service(service_, pods_) produced \n%s" % _service)
    return _service


def get_my_services(namespace_name):
    return dict((s.metadata.name, generate_my_service(s, [])) for s in get_namespace_services(namespace_name).items)


def get_my_service(namespace_name, service_name):
    return generate_my_service(get_namespace_service(namespace_name, service_name), None)


def get_namespace_services(namespace_name):
    v1 = client.CoreV1Api()
    _services = v1.list_namespaced_service(namespace_name)
    log.debug("=== get_namespace_services(%s) produced: \n%s" % (namespace_name, yaml.dump(_services)))
    return _services


def get_namespace_service(namespace_name, service_name):
    v1core = client.CoreV1Api()
    _service = v1core.read_namespaced_service(service_name, namespace_name)
    log.debug("=== get_one_service(%s, %s) produced: \n%s" % (namespace_name, service_name, yaml.dump(_service)))
    return _service
