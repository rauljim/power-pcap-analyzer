#! /usr/bin/env python

import os
import sys

PLOTTER_DIR = 'plotters'


def plot(experiment_timestamp):
    #TODO: load pickle
    for plotter_module in _get_plotter_modules():
        try:
            plotter_module.plot(experiment_timestamp)
        except:
            print plotter_module
            raise

def _get_plotter_modules():
        all_files = os.listdir(PLOTTER_DIR)
        module_names = (f[:-3] for f in all_files
                        if f[-3:] == '.py' and f[0] != '_')
        modules = [__import__('.'.join((PLOTTER_DIR, module_name)))
                .__dict__[module_name] for module_name in module_names]
        print modules
        return modules


if __name__ == '__main__':
    experiment_timestamp = sys.argv[1].split('/')[-1]
    plot(experiment_timestamp)
