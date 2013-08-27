#! /usr/bin/env python

import csv
import os
import sys
import struct

from conf import BEGIN_S, END_S


INPUT_FREQ = 5000

HEADER_LEN = 1024
FREQ = 1
STEP = 1. / FREQ
NUM_SAMPLES_PER_BUCKET = INPUT_FREQ / FREQ
MIN_VALID_SAMPLES_PER_BUCKET = 1


def pt4generator(filename):
    unpacker = struct.Struct('hH')
    with open(filename, 'rb') as pt4_file:
        header = pt4_file.read(HEADER_LEN)
        ignored_data = pt4_file.read(BEGIN_S * INPUT_FREQ * unpacker.size)
        data = pt4_file.read((END_S - BEGIN_S) * INPUT_FREQ * unpacker.size)
    unpacked_counter = 0

    power_sum = 0
    valid_samples_counter = 0
    total_avg_sum = 0
    total_avg_samples = 0
    for i in xrange(len(data) / unpacker.size):
        current_ushort, voltage_short = unpacker.unpack_from(
            data, i * unpacker.size)
        if _is_valid_sample(current_ushort, voltage_short):
            current_ma = _get_current_ma(current_ushort)
            voltage_v = _get_voltage_v(voltage_short)
            power_sum += current_ma * voltage_v
            valid_samples_counter += 1
        if i % NUM_SAMPLES_PER_BUCKET == NUM_SAMPLES_PER_BUCKET - 1:
            if valid_samples_counter < MIN_VALID_SAMPLES_PER_BUCKET:
                raise Exception('missing too many samples %f' % (i * .0002))
            timestamp = (i / NUM_SAMPLES_PER_BUCKET) * STEP
            bucket_avg = power_sum / valid_samples_counter
            yield timestamp, bucket_avg
            total_avg_sum += bucket_avg
            total_avg_samples += 1
            power_sum = 0
            valid_samples_counter = 0
    print "Total average (mw):", total_avg_sum / total_avg_samples
    raise StopIteration

def _is_valid_sample(current_ushort, voltage_short):
    return current_ushort != 0x8001 and voltage_short != 0xffff

def _get_current_ma(current_ushort):
    coarse_measurement = current_ushort & 0x01
    current_ticks = current_ushort & 0xfffe
    if coarse_measurement:
        return current_ticks * .250
    else:
        return current_ticks * .001

def _get_voltage_v(voltage_short):
    voltage_ticks = voltage_short & 0xfffc
    return voltage_ticks * .000125


def parse(experiment_timestamp):
    experiment_timestamp = experiment_timestamp.split('/')[-1]
    filename_input = os.path.join('raw', experiment_timestamp + '.pt4')
    output_dir = experiment_timestamp
    filename_output = os.path.join(output_dir, 'power_%d' % (FREQ))
    file_output = open(filename_output, 'w')

    for timestamp, power_average in pt4generator(filename_input):
        print >>file_output, '%.3f\t%d' % (timestamp,
                                           power_average)

if __name__ == '__main__':
    parse(sys.argv[1])
