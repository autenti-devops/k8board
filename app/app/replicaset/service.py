import logging

import yaml
from kubernetes import client

from .model import ReplicaSet, ReplicaSetCondition
from ..pod.service import generate_my_pod

log = logging.getLogger('replicaset')


def generate_my_replica_set(replica_set_, pods_):
    _my_replica_set = ReplicaSet(
        replica_set_.metadata.name,
        replica_set_.spec.replicas,
        replica_set_.status.replicas,
        replica_set_.status.available_replicas,
        replica_set_.status.ready_replicas,
        [ReplicaSetCondition(rsc.type, rsc.status, rsc.reason, rsc.message) for rsc in
         replica_set_.status.conditions or []],
        replica_set_.spec.selector.match_labels,
        replica_set_.metadata.labels,
        [generate_my_pod(p) for p in pods_.items or []]
    )
    log.debug('=== generate_my_replica_set(replica_set_, pods_) produced \n%s' % _my_replica_set)
    return _my_replica_set


def get_deployment_replica_sets(_deployment):
    v1apps = client.AppsV1Api()
    _label_selector = ','.join(
        '{}={}'.format(key, value) for key, value in _deployment.spec.selector.match_labels.items())
    log.info("=== deployment label selector for replicasets is: %s" % _label_selector)
    _replica_sets = v1apps.list_namespaced_replica_set(_deployment.metadata.namespace, label_selector=_label_selector)
    log.debug("=== get_deployment_replica_sets(_deployment) produced \n%s" % yaml.dump(_replica_sets))
    return _replica_sets
