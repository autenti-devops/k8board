import logging

import yaml
from kubernetes import client

from .model import Deployment, DeploymentCondition
from ..pod.service import get_replica_set_pods
from ..replicaset.service import get_deployment_replica_sets, generate_my_replica_set

log = logging.getLogger('deployment')


def generate_my_deployment(deployment_, replica_sets_):
    _deployment = Deployment(
        deployment_.metadata.name,
        deployment_.spec.replicas,
        deployment_.status.replicas,
        deployment_.status.ready_replicas,
        deployment_.status.available_replicas,
        deployment_.status.unavailable_replicas,
        deployment_.status.updated_replicas,
        [DeploymentCondition(dc.type, dc.status, dc.reason, dc.message) for dc in deployment_.status.conditions or []],
        deployment_.spec.selector.match_labels,
        deployment_.metadata.labels,
        [generate_my_replica_set(rs, get_replica_set_pods(rs)) for rs in replica_sets_ or []]
    )
    log.debug('=== generate_my_deployment(deployment_, replica_sets_) produced : \n%s' % (yaml.dump(_deployment)))
    return _deployment


def get_my_deployments(namespace_name):
    return dict(
        (d.metadata.name, generate_my_deployment(d, [])) for d in get_namespace_deployments(namespace_name).items)


def get_my_deployment(namespace_name, deployment_name):
    _deployment, _replica_sets = get_namespace_deployment(namespace_name, deployment_name)
    return generate_my_deployment(_deployment, _replica_sets.items)


def get_namespace_deployments(namespace_name):
    v1apps = client.AppsV1Api()
    _deployments = v1apps.list_namespaced_deployment(namespace_name)
    log.debug('=== get_namespace_deployments(%s) produced : \n%s' % (namespace_name, yaml.dump(_deployments)))
    return _deployments


def get_namespace_deployment(namespace_name, deployment_name):
    v1apps = client.AppsV1Api()
    _deployment = v1apps.read_namespaced_deployment(deployment_name, namespace_name)
    log.debug(
        '=== get_one_deployment(%s, %s) produced deployment : \n%s' % (
            namespace_name, deployment_name, yaml.dump(_deployment)))
    _replica_sets = get_deployment_replica_sets(_deployment)
    log.debug(
        '===get_one_deployment(%s, %s) produced replica sets: \n%s' % (
            namespace_name, deployment_name, yaml.dump(_replica_sets)))
    return _deployment, _replica_sets
