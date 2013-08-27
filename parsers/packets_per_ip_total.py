import os
import socket
import cached_lookup

output_filename = 'packets_per_ip_total.out'


class IpCounter:

    def __init__(self, ts, ip):
        self.start_ts = ts
        self.end_ts = ts
        self.ip = ip
        self.counter = 0

    def add(self, ts):
        self.end_ts = ts
        self.counter += 1

    def __repr__(self):
        hostname = cached_lookup.gethostbyaddr(self.ip)[0]
        return '%.2f\t%.2f\t%d\t%s\t%s' % (
            self.start_ts, self.end_ts, self.counter, self.ip,
            hostname)


class Parser:

    def __init__(self, output_dir):
        self.output_dir = output_dir 
        self.ip_counter_map = {}

    def incoming_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.src))

    def outgoing_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.dst))

    def handle_packet(self, ts, packet_ip):
        self.ip_counter_map.setdefault(packet_ip, IpCounter(ts, packet_ip)
                                       ).add(ts)

    def done(self, ts):
        with open(os.path.join(self.output_dir,
                                output_filename), 'w') as output_file:
            for ip_address, counter in self.ip_counter_map.iteritems():
                print >>output_file, ip_address, counter
