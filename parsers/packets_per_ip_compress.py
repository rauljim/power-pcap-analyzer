import os
import socket
import cached_lookup

output_filename = 'packets_per_ip_compress.out'

BUCKET_INTERVAL = 1
IDLE_INTERVAL = 5


class IpCounter:

    def __init__(self, ts, ip_address):
        self.start_ts = ts
        self.end_ts = ts
        self.ip_adddress = ip_address
        self.packet_counter = 0
        self.byte_counter = 0

    def add(self, ts, payload_len):
        self.end_ts = ts
        self.packet_counter += 1
        self.byte_counter += payload_len

    def __repr__(self):
        hostname = cached_lookup.gethostbyaddr(self.ip_adddress)[0]
        return '%.2f\t%.2f\t%d\t%d\t%s\t%s' % (
            self.start_ts, self.end_ts, self.packet_counter,
            self.byte_counter, self.ip_adddress,
            hostname)


class Bucket:
    def __init__(self, begin_ts):
        self.begin_ts = begin_ts
        self.end_ts = begin_ts
        self.packet_counter = 0
        self.byte_counter = 0
        self.ip_counter_map = {}

    def add(self, ts, ip_address, payload_len):
        self.end_ts = ts
        self.packet_counter += 1
        self.ip_counter_map.setdefault(ip_address, IpCounter(ts, ip_address)
                                       ).add(ts, payload_len)

    def __repr__(self):
        return '\n'.join([repr(c) for c in self.ip_counter_map.itervalues()])


class BucketManager:
    def __init__(self, output_dir):
        self.current_bucket = Bucket(0)
        self.output_file = open(os.path.join(output_dir, output_filename), 'w')

    def add(self, ts, ip_address, payload_len):
        if not self.current_bucket:
            self.current_bucket = Bucket(ts)
        if ts > self.current_bucket.end_ts + IDLE_INTERVAL:
            print >>self.output_file, 'IDLE', ts - self.current_bucket.end_ts
            if self.current_bucket.packet_counter:
                print >>self.output_file, self.current_bucket
            self.current_bucket = Bucket(ts)
        self.current_bucket.add(ts, ip_address, payload_len)
        self.last_ts = ts

    def done(self):
            print >>self.output_file, self.current_bucket


class Parser:

    def __init__(self, output_dir):
        self.bucket_manager = BucketManager(output_dir)

    def incoming_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.src),
                           len(sll_packet.data.data.data))

    def outgoing_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.dst),
                           len(sll_packet.data.data.data))

    def handle_packet(self, ts, packet_ip, payload_len):
        self.bucket_manager.add(ts, packet_ip, payload_len)

    def done(self, ts):
        self.bucket_manager.done()
