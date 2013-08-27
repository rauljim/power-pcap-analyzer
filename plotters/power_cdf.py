from matplotlib import pyplot
import csv
import os


POWER_FREQ = 1
output_filename = 'power_cdf.png'


def plot(experiment_timestamp):
    power_x, power_y = get_power_cdf(experiment_timestamp)
    x, y = get_total_packets(experiment_timestamp)
    figure = pyplot.figure()
    grid1x1 = 111
    power_plot = figure.add_subplot(grid1x1)
    power_plot.plot(power_x, power_y, 'b-')
    power_plot.set_ylabel('power (mw)', color='b')

    fullpath = os.path.join(experiment_timestamp, output_filename)
    print 'Generating plot:', fullpath
    pyplot.savefig(fullpath)


def get_power_cdf(experiment_timestamp):
    timestamps = []
    power_mw = []
    filename = '_'.join(('power', str(POWER_FREQ)))
    with open(os.path.join(experiment_timestamp, filename)) as csvfile:
        for ts, power in csv.reader(csvfile, delimiter='\t'):
            power_mw.append(float(power))
    power_mw.sort()
    step = 1./len(power_mw)
    p = [i*step for i in range(len(power_mw))]
    return power_mw, p


def get_total_packets(experiment_timestamp):
    x = []
    y = []
    with open(os.path.join(experiment_timestamp, 'packets')) as csvfile:
        for (ts,
             packets_sent, _,
             packets_received, _
             ) in csv.reader(csvfile, delimiter='\t'):
            x.append(float(ts))
            y.append(int(packets_sent) + int(packets_received))
    return x, y
