import logging

import yaml
from kubernetes import client

from .model import Pod, PodCondition, PodContainerSpec, PodContainerSpecPort, PodContainerSpecEnvironment, \
    PodContainerStatus

log = logging.getLogger('pod')


def generate_my_pod(_pod):
    my_pod_ = Pod(
        _pod.metadata.name,
        _pod.status.phase,
        _pod.status.pod_ip,
        [PodContainerSpec(
            pc.name,
            pc.image,
            pc.image_pull_policy,
            pc.command,
            [PodContainerSpecPort(
                pcp.container_port,
                pcp.protocol
            ) for pcp in pc.ports or []],
            pc.resources.limits,
            pc.resources.requests,
            [PodContainerSpecEnvironment(
                pce.name,
                pce.value,
                pce.value_from
            ) for pce in pc.env or []]
        ) for pc in _pod.spec.containers or []],
        _pod.metadata.labels,
        [PodCondition(
            pc.type,
            pc.status,
            pc.reason,
            pc.message
        ) for pc in _pod.status.conditions or []],
        [PodContainerStatus(
            pcs.name,
            pcs.image,
            pcs.ready,
            pcs.restart_count,
            pcs.state.running.started_at if pcs.state.running is not None else None,
            pcs.state.waiting.reason if pcs.state.waiting is not None else None,
            pcs.state.waiting.message if pcs.state.waiting is not None else None
        ) for pcs in
            _pod.status.container_statuses or []]
    )
    log.debug('=== generate_my_pod(_pod) produced: \n%s' % yaml.dump(my_pod_))
    return my_pod_


def get_my_pod(namespace_name, pod_name):
    return generate_my_pod(get_namespace_pod(namespace_name, pod_name))


def get_replica_set_pods(_replica_set):
    v1core = client.CoreV1Api()
    _label_selector = ','.join(
        '{}={}'.format(key, value) for key, value in _replica_set.spec.selector.match_labels.items())
    log.info("=== replicaSet label selector for pods is: %s" % _label_selector)
    _pods = v1core.list_namespaced_pod(_replica_set.metadata.namespace, label_selector=_label_selector)
    log.debug('=== get_replica_set_pods(_replica_set) produced \n%s' % yaml.dump(_pods))
    return _pods


def get_service_pods(_service):
    v1core = client.CoreV1Api()
    _label_selector = ','.join(
        '{}={}'.format(key, value) for key, value in _service.spec.selector.items())
    log.info("=== service label selector for pods is: %s" % _label_selector)
    _pods = v1core.list_namespaced_pod(_service.metadata.namespace, label_selector=_label_selector)
    log.debug('=== get_service_pods(_service) produced: \n%s' % yaml.dump(_pods))
    return _pods.items


def get_namespace_pod(namespace_name, pod_name):
    v1core = client.CoreV1Api()
    _pod = v1core.read_namespaced_pod(pod_name, namespace_name)
    log.debug('=== get_namespace_pod(%s, %s) produced: \n%s' % (namespace_name, pod_name, yaml.dump(_pod)))
    return _pod


def get_pod_logs(namespace_name, pod_name, container_name):
    v1core = client.CoreV1Api()
    _log = v1core.read_namespaced_pod_log(pod_name, namespace_name, container=container_name, tail_lines=1000)
    return _log


def delete_namespace_pod(namespace_name, pod_name):
    v1core = client.CoreV1Api()
    log.info('=== delete_namespace_pod(%s, %s) will perform deletion.' % (namespace_name, pod_name))
    _status = v1core.delete_namespaced_pod(pod_name, namespace_name)
    log.debug(
        '=== delete_namespace_pod(%s, %s) deleted pod with output status: \n%s.' % (namespace_name, pod_name, _status))
