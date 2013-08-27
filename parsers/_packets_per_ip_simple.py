import socket


class Parser:

    def __init__(self):
        self.last_ip = None
        self.packet_counter = 0

    def incoming_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.src))

    def outgoing_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.dst))

    def handle_packet(self, ts, packet_ip):
        if packet_ip == self.last_ip:
            self.packet_counter += 1
        else:
            print self.packet_counter, ts
            print ts, packet_ip,

            self.last_ip = packet_ip
            self.packet_counter = 0

    def done(self, ts):
        print self.packet_counter, ts
