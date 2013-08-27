#! /usr/bin/env python


import sys

from socket import inet_ntoa, ntohs
import os
import time

import pcap
import dpkt

import parsers.cached_lookup
from conf import BEGIN_S, END_S

PARSER_DIR = 'parsers'

UNICAST_TO_US = 0
SENT_BY_US = 4


class Multiparser(object):

    def __init__(self, output_dir):
        parsers.cached_lookup.load()
        parser_modules = self._get_parser_modules()
        self.parsers = []
        for module in parser_modules:
            try:
                self.parsers.append(module.Parser(output_dir))
            except (AttributeError):
                print module, "not a parser"

    def handle_packet(self, ts, sll_packet, eth_packet):
        SAMSUNG_PREFIX = '\xa0\x0b\xba'
        outgoing_handlers = (parser.outgoing_packet for parser in self.parsers)
        incoming_handlers = (parser.incoming_packet for parser in self.parsers)
        sll_type = sll_packet.type
        if sll_type == SENT_BY_US:
            packet = sll_packet
            handlers = outgoing_handlers
        elif sll_type == UNICAST_TO_US:
            packet = sll_packet
            handlers = incoming_handlers
        else:
            #ethernet
            if eth_packet.src.startswith(SAMSUNG_PREFIX):
                packet = eth_packet
                handlers = outgoing_handlers
            elif eth_packet.dst.startswith(SAMSUNG_PREFIX):
                packet = eth_packet
                handlers = incoming_handlers
            else:
                print 'bad packet (probably ARP). Inspect ts:', ts + 30
                
        try:
            packet.ip
        except:
            print 'no IP'
            return
        for handler in handlers:
            handler(ts, packet)
            
    def done(self, ts):
        parsers.cached_lookup.save()
        for parser in self.parsers:
            parser.done(ts)

    def _get_parser_modules(self):
        all_files = os.listdir(PARSER_DIR)
        module_names = (f[:-3] for f in all_files if f[-3:] == '.py' and f[0] != '_' and not f.startswith('cache'))
        return [__import__('.'.join((PARSER_DIR, module_name))).__dict__[module_name] for module_name in module_names]


def parse(experiment_timestamp):
    experiment_timestamp = experiment_timestamp.split('/')[-1] 
    output_dir = experiment_timestamp
    try:
        os.mkdir(output_dir)
    except (OSError):
        raw_input("Directory exists. Everything will be overwritten. OK?")
        
    multiparser = Multiparser(output_dir)
    start_ts = 0
    pcap_filename = os.path.join('raw', experiment_timestamp + '.pcap')
    for ts_absolute, frame in pcap.pcap(pcap_filename):
        if not start_ts:
            start_ts = ts_absolute + BEGIN_S
        ts = ts_absolute - start_ts # ts relative to start
        if ts < 0:
            continue # packet sent before power measurement started
        if ts > END_S - BEGIN_S:
            break # we're done
        sll_packet = dpkt.sll.SLL(frame)
        eth_packet = dpkt.ethernet.Ethernet(frame)
        multiparser.handle_packet(ts, sll_packet, eth_packet)
    multiparser.done(ts)
    

if __name__ == '__main__':
    experiment_timestamp = sys.argv[1].split('.')[0]
    parse(experiment_timestamp)
