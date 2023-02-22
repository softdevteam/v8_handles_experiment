import json
import sys
import pprint
import math
import os
from statistics import geometric_mean, stdev

def process_speedometer(results_file, pexecs):
    results = {}

    unwanted = ['score']
    with open(results_file) as f:
        data = json.load(f)
        for browser_name, browser in data.items():
            for bm, runs in browser['data'].items():
                # We only want the totals
                if len(bm.split('/')) > 2 or any([x in bm for x in unwanted]):
                    continue

                bm_name = bm if bm != "mean" else "geometric mean"
                if bm_name not in results:
                    results[bm_name] = {}
                results[bm_name][browser_name] = {
                    'mean' : runs['average'],
                    'geomean' : runs['geomean'],
                    'stddev' : runs['stddev'],
                }


    with open("table_no_gc.tex", "w") as f:
        for bm, browsers in results.items():
            f.write("%s " % bm)
            for b, data in browsers.items():
                if "mean" in bm:
                    f.write("& %.3f " % data['geomean'])
                else:
                    f.write("& %.3f ± %.6f " % \
                            (data['mean'], \
                            confidence_interval(data['mean'], data['stddev'], pexecs)))
            f.write(" \\\\\n")

def confidence_interval(mean, stddev, num_samples):
    Z = 2.576  # 99% interval
    return Z * (stddev / math.sqrt(num_samples))

if __name__ == "__main__":
    results = "crossbench_no_gc/speedometer_2.1.json"
    process_speedometer(results, 10)


