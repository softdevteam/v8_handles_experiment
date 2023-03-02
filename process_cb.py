import json
import sys
import pprint
import math
import os

def process(results_dir):
    assert len(os.listdir(results_dir)) == 2

    min_cfg = [d for d in os.listdir(results_dir) if "min" in d][0]
    no_compact_cfg = [d for d in os.listdir(results_dir) if "no_compact" in d][0]

    try:
        os.remove("experimentstats.tex")
    except OSError:
        pass

    min_ = Results(os.path.join(results_dir, min_cfg), "min")
    min_.gen_commands("experimentstats.tex", gen_story_names = True)
    min_.gen_table("table_min.tex")

    no_compact = Results(os.path.join(results_dir, no_compact_cfg), "nocompact")
    no_compact.gen_commands("experimentstats.tex")
    no_compact.gen_table("table_no_stack_compact.tex")

class Results:
    def __init__(self, results_file, configuration):
        self.configuration = configuration
        self.direct = {}
        self.handles = {}
        self.pexecs = None
        self.parse_results(os.path.join(results_file, "speedometer_2.1.json"))

    def parse_results(self, results_file):
        results = {}
        self.latex_names = {}

        wanted = ['total']
        with open(results_file) as f:
            data = json.load(f)

            # We only parse results which compare 2 browser configs
            assert len(data) == 2

            for browser_name, browser in data.items():

                results = {}
                for bm, runs in browser['data'].items():
                    # We only want the totals
                    if len(bm.split('/')) > 2 or not any([x in bm for x in wanted]):
                        continue


                    if bm == "total":
                        bm_name = bm
                    else:
                        bm_name = ''.join(s for s in bm[:-14]
                                                if s.isalpha()).lower().replace("-","")
                    ltx = bm[:-14]
                    if bm_name not in results:
                        if bm != "total":
                            self.latex_names[bm_name] = ltx
                        results[bm_name] = {}

                    if self.pexecs == None:
                        self.pexecs = len(runs['values'])

                    assert self.pexecs == len(runs['values'])

                    results[bm_name] = {
                        'mean' : runs['average'],
                        'geomean' : runs['geomean'],
                        'stddev' : runs['stddev'],
                    }

                if "handles" in browser_name:
                    self.handles = results
                else:
                    self.direct = results



    def gen_commands(self, commands_file, gen_story_names = False):
        with open(commands_file, "a") as cmds:
            if gen_story_names:
                cmds.write("% speedometer story names\n")
                for cmd, ltx in self.latex_names.items():
                    cmds.write("\\newcommand\\%s{\\textrm{%s}\\xspace}\n" % (cmd, ltx))

            cmds.write("\n% speedometer story percentage diffs\n")
            for bm in self.handles:
                # Put the percent diff in the commands
                cmds.write('\\newcommand\\%s%spdiff{%.2f\\xspace}\n' % (\
                        self.configuration, \
                        bm, \
                        (pdiff(float(self.handles[bm]['mean']),
                               float(self.direct[bm]['mean'])))))

    def gen_table(self, table_file):
        with open(table_file, "w") as table:
            for bm in self.handles:
                label = "\\%s" % bm
                if "total" in bm:
                    label = "Total "
                    table.write("\\midrule\n")
                table.write("%s & %.3f ± %.6f & %.3f ± %.6f  \\\\\n" % (\
                        label, \
                        self.handles[bm]['mean'], \
                        confidence_interval(self.handles[bm]['mean'],
                                            self.handles[bm]['stddev'],
                                            self.pexecs),
                        self.direct[bm]['mean'], \
                        confidence_interval(self.direct[bm]['mean'],
                                            self.direct[bm]['stddev'],
                                            self.pexecs)))


def pdiff(a, b):
    return ((a - b) / a) * 100

def confidence_interval(mean, stddev, num_samples):
    Z = 2.576  # 99% interval
    return Z * (stddev / math.sqrt(num_samples))

if __name__ == "__main__":
    results_dir = os.path.join(sys.argv[1])
    process(results_dir)

