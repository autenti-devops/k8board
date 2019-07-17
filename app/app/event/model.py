class Event:
    def __init__(self, count, message, last_timestamp, reason, ctype, involved_object_kind, involved_object_name):
        self.count = count
        self.message = message
        self.last_timestamp = last_timestamp
        self.reason = reason
        self.type = ctype
        self.involved_object_kind = involved_object_kind
        self.involved_object_name = involved_object_name
