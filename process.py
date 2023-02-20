import json
import sys
import pprint
import math
import os
from statistics import geometric_mean, stdev

def process_speedometer(results_dir):
    handle_dirs = sorted([d for d in os.listdir(results_dir) if "Handles" in d])
    direct_dirs = sorted([d for d in os.listdir(results_dir) if "Direct_Pointers" in d])

    if len(handle_dirs) > 1:
        print("==> %s benchmark results for Handles found. Using %s" %
              (len(handle_dirs), handle_dirs[-1]))

    if len(direct_dirs) > 1:
        print("==> %s benchmark results for Direct_Pointers found. Using %s" %
              (len(direct_dirs), direct_dirs[-1]))

    handle_data = read_measurements(os.path.join(results_dir, handle_dirs[-1]))
    direct_data = read_measurements(os.path.join(results_dir, direct_dirs[-1]))

    with open("table.tex", "w") as f:
        for (h, d) in zip(handle_data.items(), direct_data.items()):
            assert h[0] == d[0]
            f.write("%s & %.3f ± %.6f & %.3f ± %.6f \\\\\n" % \
                    (h[0], \
                     mean(h[1]), \
                     confidence_interval(h[1]), \
                     mean(d[1]), \
                     confidence_interval(d[1])))

def read_measurements(d):
    results = {}
    for pexec_dir in os.listdir(d):
        if "Speedometer2" not in pexec_dir:
            continue
        file = os.path.join(d, pexec_dir, "measurements.json")
        with open(file) as f:
            pexec = json.load(f)

            for bm, samples in pexec['measurements'].items():
                if bm not in results:
                    results[bm] = []
                for sample in samples['samples']:
                    results[bm].append(sample)
    return results


def confidence_interval(samples):
    Z = 2.576  # 99% interval
    return Z * (stdev(samples) / math.sqrt(len(samples)))

def mean(l):
    return math.fsum(l) / float(len(l))

if __name__ == "__main__":
    results ="/home/jake/research/v8_handles_experiments/results/artifacts/"
    process_speedometer(results)


