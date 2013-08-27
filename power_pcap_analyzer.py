#! /usr/bin/env python

import pcap_parser
import power_parser
import sys
import plotter


if __name__ == '__main__':
    experiment_timestamp = sys.argv[1].split('/')[-1]
    pcap_parser.parse(experiment_timestamp)
    power_parser.parse(experiment_timestamp)
    plotter.plot(experiment_timestamp)
