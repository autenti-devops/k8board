class Deployment:
    def __init__(
            self, name, desired_replicas, existing_replicas, ready_replicas, available_replicas, unavailable_replicas,
            updated_replicas, conditions, selector, labels, replica_sets):
        self.name = name
        self.desired_replicas = desired_replicas or 0
        self.existing_replicas = existing_replicas or 0
        self.ready_replicas = ready_replicas or 0
        self.available_replicas = available_replicas or 0
        self.unavailable_replicas = unavailable_replicas or 0
        self.updated_replicas = updated_replicas or 0
        self.conditions = conditions
        self.selector = selector
        self.labels = labels
        self.correctness = "{:.0%}".format(
            self.available_replicas / self.desired_replicas) if self.existing_replicas != 0 else '100%'
        self.replica_sets = replica_sets


class DeploymentCondition:
    def __init__(self, ctype, status, reason, message):
        self.type = ctype
        self.status = status
        self.reason = reason
        self.message = message
