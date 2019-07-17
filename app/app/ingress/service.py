import logging

import yaml
from kubernetes import client

from .model import Ingress, IngressRule, IngressPath

log = logging.getLogger('ingress')


def generate_my_ingress(ingress_):
    _ingress = Ingress(
        ingress_.metadata.name,
        ingress_.metadata.labels,
        [IngressRule(ir.host, [IngressPath(ip.path, ip.backend.service_name, ip.backend.service_port) for ip in
                               ir.http.paths or []]) for ir in ingress_.spec.rules or []]
    )
    log.debug('=== generate_my_ingress(ingress_) produced: \n%s' % yaml.dump(_ingress))
    return _ingress


def get_my_ingresses(namespace_name):
    return dict((i.metadata.name, generate_my_ingress(i)) for i in get_namespace_ingresses(namespace_name).items)


def get_my_ingress(namespace_name, ingress_name):
    return generate_my_ingress(get_namespace_ingress(namespace_name, ingress_name))


def get_namespace_ingresses(namespace_name):
    v1b1 = client.ExtensionsV1beta1Api()
    _ingresses = v1b1.list_namespaced_ingress(namespace_name)
    log.debug('=== get_namespace_ingresses(%s) produced \n%s' % (namespace_name, yaml.dump(_ingresses)))
    return _ingresses


def get_namespace_ingress(namespace_name, ingress_name):
    v1b1 = client.ExtensionsV1beta1Api()
    _ingress = v1b1.read_namespaced_ingress(ingress_name, namespace_name)
    log.debug('=== get_namespace_ingress(%s, %s) produced \n %s' % (namespace_name, ingress_name, _ingress))
    return _ingress
