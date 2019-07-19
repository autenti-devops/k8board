class Pod:
    def __init__(self, name, phase, ip, containers, labels, conditions, containers_statuses):
        self.name = name
        self.phase = phase
        self.ip = ip
        self.containers = containers
        self.labels = labels
        self.conditions = conditions
        self.containers_statuses = containers_statuses


class PodCondition:
    def __init__(self, ctype, status, reason, message):
        self.type = ctype
        self.status = status
        self.reason = reason
        self.message = message


class PodContainerStatus:
    def __init__(self, name, image, ready, restart_count, started_at, waiting_reason, waiting_message):
        self.name = name
        self.image = image
        self.ready = ready
        self.restart_count = restart_count
        self.started_at = started_at
        self.waiting_reason = waiting_reason
        self.waiting_message = waiting_message


class PodContainerSpec:
    def __init__(self, name, image, image_pull_policy, command, ports, limits,
                 requests, environments):
        self.name = name
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.command = command
        self.ports = ports
        self.limits = limits
        self.requests = requests
        self.environments = environments


class PodContainerSpecEnvironment:
    def __init__(self, name, value, value_from):
        self.name = name
        self.value = value
        self.value_from = value_from


class PodContainerSpecPort:
    def __init__(self, container_port, protocol):
        self.container_port = container_port
        self.protocol = protocol
