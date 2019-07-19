class Service:
    def __init__(self, name, ports, selector, labels, pods):
        self.name = name
        self.ports = ports
        self.selector = selector
        self.labels = labels
        self.pods = pods


class ServicePort:
    def __init__(self, name, port, protocol, target_port):
        self.name = name
        self.port = port
        self.protocol = protocol
        self.target_port = target_port
