from matplotlib import pyplot
import csv
import os


POWER_FREQ = 5
output_filename = 'many_power_cdf.png'

EXPERIMENT_LABEL_TIMESTAMPS = (
    ('wifi baseline (304)', '201306201525',   'k:'),#131430'),
    ('wifi leecher  (326)', '201306201300',   'k--'),#191050'),
    ('wifi peer       (333)', '201306201415', 'k-'),#190900'),
    ('3G  baseline (455)', '201306201120',  'r:'),#131510'),
    ('3G  leecher  (513)', '201306201335',  'r--'),#171520'),
    ('3G  peer      (841)', '201306201450', 'r-'),#190935'),
    )

def plot():
    figure = pyplot.figure()
    grid1x1 = 111
    power_plot = figure.add_subplot(grid1x1)
    power_plot.set_xlabel('power (mW)')
    power_plot.set_ylabel('CDF')
    for label, experiment_timestamp, style in EXPERIMENT_LABEL_TIMESTAMPS:
        power_x, power_y = get_power_cdf(experiment_timestamp)
        x, y = get_total_packets(experiment_timestamp)
        power_plot.plot(power_x, power_y, style, label=label, markevery=30)

    pyplot.legend(loc='lower right')
    fullpath = output_filename
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

if __name__ == '__main__':
    plot()
