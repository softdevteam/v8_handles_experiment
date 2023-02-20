#! /bin/sh

CHROMIUM_DIR=/home/jake/research/chromium/src/
RESULTS_DIR=`pwd`/results/
PEXECS=10

mkdir -p ${RESULTS_DIR}
cd ${CHROMIUM_DIR}

tools/perf/run_benchmark run --browser=exact \
    --browser-executable=out/baseline/content_shell speedometer2 \
    --pageset-repeat=${PEXECS} \
    --results-label="Handles" \
    --use-live-sites \
    --output-format json-test-results \
    --output-format csv \
    --output-dir=${RESULTS_DIR} \
    --output-format html \
    --reset-results

tools/perf/run_benchmark run --browser=exact \
    --browser-executable=out/direct_handles_release/content_shell speedometer2 \
    --pageset-repeat=${PEXECS} \
    --results-label="Direct Pointers" \
    --output-format json-test-results \
    --output-format csv \
    --output-dir=${RESULTS_DIR} \
    --output-format html \
    --use-live-sites
