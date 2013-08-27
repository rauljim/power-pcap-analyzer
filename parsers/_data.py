class Power(object):
    def __init__(self):
        self.timestamps = []
        self.power_mw = []


class PacketCounter(object):
    def __init__(self):
        self.timestamps = []
        self.received_packets = []
        self.received_bytes = []
        self.sent_packets = []
        self.sent_bytes = []
