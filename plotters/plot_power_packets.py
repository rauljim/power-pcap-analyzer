from matplotlib import pyplot
import csv
import os


POWER_FREQ = 1
output_filename = 'power_vs_packets.png'
output_filename2 = 'power_vs_bytes.png'


class NetworkTraffic(object):
    def __init__(self, experiment_timestamp):
        self.timestamps = []
        self.packets_received = []
        self.packets_sent = []
        self.packets_total = []
        self.bytes_received = []
        self.bytes_received_cum = []
        self.bytes_sent = []
        self.bytes_sent_cum = []
        with open(os.path.join(experiment_timestamp, 'packets')) as csvfile:
            bytes_sent_cum = 0
            bytes_received_cum = 0
            for splitted_line in csv.reader(csvfile, delimiter='\t'):
                self.timestamps.append(float(splitted_line[0]))
                (packets_sent,
                packets_received,
                bytes_sent,
                bytes_received) = map(int, splitted_line[1:])
                self.packets_total.append(packets_sent + packets_received)
                bytes_sent_cum += bytes_sent / 1000000.
                bytes_received_cum += bytes_received / 1000000.
                self.bytes_sent_cum.append(bytes_sent_cum)
                self.bytes_received_cum.append(bytes_received_cum)
        print bytes_sent_cum
        print bytes_received_cum


def plot(experiment_timestamp):
    power_x, power_y = get_power_samples_stair(experiment_timestamp)
    network_traffic = NetworkTraffic(experiment_timestamp)
    figure = pyplot.figure()
    grid1x1 = 111
    power_plot = figure.add_subplot(grid1x1)
    power_plot.plot(power_x, power_y, 'b-')
    power_plot.set_ylabel('power (mW)', color='b')

    traffic_plot = power_plot.twinx()
    traffic_plot.semilogy(network_traffic.timestamps,
                         network_traffic.packets_total,
                         'ro')
    traffic_plot.set_ylabel('packets', color='r')
    fullpath = os.path.join(experiment_timestamp, output_filename)
    print 'Generating plot:', fullpath
    pyplot.savefig(fullpath)


    figure = pyplot.figure()
    grid1x1 = 111
    power_plot = figure.add_subplot(grid1x1)
    power_plot.plot(power_x, power_y, 'b-')
    power_plot.set_ylabel('power (mw)', color='b')

    traffic_plot = power_plot.twinx().twiny()
    traffic_plot.plot(network_traffic.timestamps,
                         network_traffic.bytes_sent_cum,
                         'g-')
    traffic_plot.plot(network_traffic.timestamps,
                      network_traffic.bytes_received_cum,
                      'k-')
    fullpath = os.path.join(experiment_timestamp, output_filename2)
    print 'Generating plot:', fullpath
    pyplot.savefig(fullpath)


def get_power_samples_stair(experiment_timestamp):
    timestamps = []
    power_mw = []
    filename = '_'.join(('power', str(POWER_FREQ)))
    with open(os.path.join(experiment_timestamp, filename)) as csvfile:
        for ts, power in csv.reader(csvfile, delimiter='\t'):
            timestamps.append(float(ts))
            power_mw.append(float(power))
            timestamps.append(float(ts) + 1./POWER_FREQ)
            power_mw.append(float(power))
    return timestamps, power_mw
