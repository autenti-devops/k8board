import logging

from kubernetes import client

log = logging.getLogger('namespace')


def get_namespaces_names():
    v1 = client.CoreV1Api()
    _namespaces = v1.list_namespace().items
    _filtered_namespaces_names = [n.metadata.name for n in _namespaces if
                                  n.metadata.annotations and 'k8board/list' in n.metadata.annotations and
                                  n.metadata.annotations['k8board/list'] == 'true' or []]
    log.debug('=== get_namespaces() produced: \n%s' % _filtered_namespaces_names)
    return _filtered_namespaces_names
