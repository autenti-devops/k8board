class ReplicaSet:
    def __init__(self, name, desired_replicas, existing_replicas, available_replicas, ready_replicas, conditions,
                 selector, labels, pods):
        self.name = name
        self.desired_replicas = desired_replicas or 0
        self.existing_replicas = existing_replicas or 0
        self.available_replicas = available_replicas or 0
        self.ready_replicas = ready_replicas or 0
        self.conditions = conditions
        self.selector = selector
        self.labels = labels
        self.pods = pods


class ReplicaSetCondition:
    def __init__(self, ctype, status, reason, message):
        self.type = ctype
        self.status = status
        self.reason = reason
        self.message = message
