import json
import sys
import pprint
import math
import os
from statistics import geometric_mean, stdev

def process_speedometer(results_file, pexecs):
    results = {}
    geomeans = {}

    wanted = ['total', 'geomean']
    with open(results_file) as f:
        data = json.load(f)
        for browser_name, browser in data.items():
            for bm, runs in browser['data'].items():
                # We only want the totals
                if len(bm.split('/')) > 2 or not any([x in bm for x in wanted]):
                    continue

                if bm == "geomean":
                    geomeans[browser_name] = runs['geomean']
                    continue

                if bm not in results:
                    results[bm] = {}

                results[bm][browser_name] = {
                    'mean' : runs['average'],
                    'geomean' : runs['geomean'],
                    'stddev' : runs['stddev'],
                }

    gen_table(results, geomeans, pexecs)


def gen_table(results, geomeans, pexecs):
    with open("table_no_gc.tex", "w") as f:
        for bm, browsers in results.items():
            f.write("%s " % bm)
            for b, data in browsers.items():
                f.write("& %.3f ± %.6f " % \
                        (data['mean'], \
                        confidence_interval(data['mean'], data['stddev'], pexecs)))
            f.write(" \\\\\n")
        f.write("geometric mean ")
        for browser, gmean in geomeans.items():
            f.write("& %.3f " % gmean)
        f.write(" \\\\\n")

def confidence_interval(mean, stddev, num_samples):
    Z = 2.576  # 99% interval
    return Z * (stddev / math.sqrt(num_samples))

if __name__ == "__main__":
    results = "crossbench_no_gc/speedometer_2.1.json"
    process_speedometer(results, 10)


