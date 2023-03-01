import json
import sys
import pprint
import math
import os

def process_speedometer(results_file, pexecs, table_name):
    results = {}
    totals = {}

    wanted = ['total']
    with open(results_file) as f:
        data = json.load(f)
        for browser_name, browser in data.items():
            for bm, runs in browser['data'].items():
                # We only want the totals
                if len(bm.split('/')) > 2 or not any([x in bm for x in wanted]):
                    continue

                if bm == "total":
                    totals[browser_name] = runs
                    continue

                if bm not in results:
                    results[bm] = {}

                assert len(runs['values']) == pexecs

                results[bm][browser_name] = {
                    'mean' : runs['average'],
                    'geomean' : runs['geomean'],
                    'stddev' : runs['stddev'],
                }

    with open(table_name, "w") as f:
        for bm, browsers in results.items():
            f.write("%s " % bm)
            for b, data in browsers.items():
                f.write("& %.3f ± %.6f " % \
                        (data['mean'], \
                        confidence_interval(data['mean'], data['stddev'], pexecs)))
            f.write(" \\\\\n")
        f.write("\\midrule\n")
        f.write("Total")
        for browser, total in totals.items():
            f.write("& %.3f " % confidence_interval(total['average'], total['stddev'], pexecs))
        f.write(" \\\\\n")

def confidence_interval(mean, stddev, num_samples):
    Z = 2.576  # 99% interval
    return Z * (stddev / math.sqrt(num_samples))

if __name__ == "__main__":
    file = os.path.join(sys.argv[1], "speedometer_2.1.json")
    pexecs = int(sys.argv[2])
    table_name = sys.argv[3]
    process_speedometer(file, pexecs, table_name)


