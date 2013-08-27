import os
import socket
import cached_lookup

output_filename = 'packets_per_ip.out'

BUCKET_INTERVAL = 1


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
        return '%f.2\t%f.2\t%d\t%s\t%s' % (
            self.start_ts, self.end_ts, self.counter, self.ip,
            hostname)


class Bucket:
    def __init__(self, begin_ts):
        self.begin_ts = begin_ts
        self.next_ts = begin_ts + BUCKET_INTERVAL
        self.packet_counter = 0
        self.ip_counter_map = {}

    def add(self, ts, packet_ip):
        self.packet_counter += 1
        self.ip_counter_map.setdefault(packet_ip, IpCounter(ts, packet_ip)
                                       ).add(ts)

    def __repr__(self):
        return '\n'.join([repr(c) for c in self.ip_counter_map.itervalues()])


class BucketManager:
    def __init__(self, output_dir):
        self.output_file = open(os.path.join(output_dir, output_filename), 'w')
        self.current_bucket = Bucket(0)

    def add(self, ts, packet_ip):
        if not self.current_bucket:
            self.current_bucket = Bucket(ts)
        while ts > self.current_bucket.next_ts:
            if self.current_bucket.packet_counter:
                print >>self.output_file, self.current_bucket
            self.current_bucket = Bucket(self.current_bucket.next_ts)
        self.current_bucket.add(ts, packet_ip)
        self.last_ts = ts

    def done(self):
            print >>self.output_file, self.current_bucket


class Parser:

    def __init__(self, output_dir):
        self.bucket_manager = BucketManager(output_dir)

    def incoming_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.src))

    def outgoing_packet(self, ts, sll_packet):
        self.handle_packet(ts, socket.inet_ntoa(sll_packet.ip.dst))

    def handle_packet(self, ts, packet_ip):
        self.bucket_manager.add(ts, packet_ip)

    def done(self, ts):
        self.bucket_manager.done()
