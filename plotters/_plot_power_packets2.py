from matplotlib import pyplot
import csv
import os


POWER_FREQ = 1
output_filename = 'power_vs_packets.eps'


class StairPowerData:
    def __init__(self):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x.append(x)
        self.x.append(x + .999)
        self.y.append(y)
        self.y.append(y)


def plot(experiment_timestamp):
    power_plotdata = get_power_plotdata_stair(experiment_timestamp)
    x = []
    y = []
    with open(os.path.join(experiment_timestamp, 'packets')) as csvfile:
        for ts, packets in csv.reader(csvfile, delimiter='\t'):
            x.append(float(ts))
            y.append(int(packets))




    figure = pyplot.figure()
    grid1x1 = 111
    power_plot = figure.add_subplot(grid1x1)
    power_plot.plot(power_x, power_y, 'b-')
    power_plot.set_ylabel('power (mw)', color='b')

    packet_plot = power_plot.twinx()
    packet_plot.semilogy(x, y, 'ro')
    packet_plot.set_ylabel('packets (within 0.1s)', color='r')
    fullpath = os.path.join(experiment_timestamp, output_filename)
    print 'Generating plot:', fullpath
    pyplot.savefig(fullpath)



class PlottingData:
    def __init__(self, experiment_timestamp):
        self.experiment_timestamp = experiment_timestamp
        self.power_data = StairPowerData()

    def add_power_sample(self, ts, power):
        self.power_data.add(ts, power)

    def add_packet_sample(self, ts, packets_sent, bytes_sent, packets_received, bytes_received):
        pass
    
    def done(self):
        