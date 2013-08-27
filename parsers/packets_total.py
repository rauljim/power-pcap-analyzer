import os

output_filename = 'packets'
# FORMAT:
# start timestamp
# packets sent
# packets received
# bytes sent
# bytes received

RECEIVED = 'r'
SENT = 's'
BUCKET_INTERVAL = 1


class Bucket:
    def __init__(self, begin_ts):
        self.start_ts = begin_ts
        self.end_ts = begin_ts
        self.packet_counter = {SENT: 0,
                               RECEIVED: 0}
        self.byte_counter = {SENT: 0,
                             RECEIVED: 0}

    def add(self, ts, payload_len, sent_or_received):
        self.end_ts = ts
        self.packet_counter[sent_or_received] += 1
        self.byte_counter[sent_or_received] += payload_len

    def __repr__(self):
        return '%.2f\t%d\t%d\t%d\t%d' % (self.start_ts,
                                         self.packet_counter[SENT],
                                         self.packet_counter[RECEIVED],
                                         self.byte_counter[SENT],
                                         self.byte_counter[RECEIVED],
                                         )


class BucketManager:
    def __init__(self, output_dir):
        self.output_file = open(os.path.join(output_dir, output_filename), 'w')
        self.current_bucket = Bucket(0)

    def add(self, ts, payload_len, sent_or_received):
#        if not self.current_bucket:
#            self.current_bucket = Bucket(ts)
        if ts > self.current_bucket.start_ts + BUCKET_INTERVAL:
            if self.current_bucket.packet_counter:
                print >>self.output_file, self.current_bucket
            self.current_bucket = Bucket(ts)
        self.current_bucket.add(ts, payload_len, sent_or_received)
        self.last_ts = ts

    def done(self):
            print >>self.output_file, self.current_bucket


class Parser:

    def __init__(self, output_dir):
        self.bucket_manager = BucketManager(output_dir)

    def incoming_packet(self, ts, sll_packet):
        self.handle_packet(ts, len(sll_packet.data.data.data), RECEIVED)

    def outgoing_packet(self, ts, sll_packet):
        self.handle_packet(ts, len(sll_packet.data.data.data), SENT)

    def handle_packet(self, ts, payload_len, sent_or_received):
        self.bucket_manager.add(ts, payload_len, sent_or_received)

    def done(self, ts):
        self.bucket_manager.done()
