class Ingress:
    def __init__(self, name, labels, rules):
        self.name = name
        self.labels = labels
        self.rules = rules


class IngressRule:
    def __init__(self, host, paths):
        self.host = host
        self.paths = paths


class IngressPath:
    def __init__(self, path, service_name, service_port):
        self.path = path
        self.service_name = service_name
        self.service_port = service_port
