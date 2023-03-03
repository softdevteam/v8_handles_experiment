# Experiment for "Moving from Handles to Direct References Improves VM Performance"

This is the experiment for the paper ["Moving from Handles to Direct References
Improves VM Performance"](#). The repository for the paper can be found at
https://github.com/softdevteam/v8_handles_paper.

## Installing dependencies

To build the tables and latex macros from the experiments on your local machine,
you need to install LaTeX, Python 3.7 (or later).

## Running the experiment

When you have installed the dependencies, simply run:

```
make all
```

This produces a number of `.tex` files.  You can examine these individually, or
you can rebuild our paper with the data from your run by first downloading the
paper source:

```
git clone https://github.com/softdevteam/v8_handles_paper
cd v8_handles_paper
```

Copy the `.tex` files you have created into the root of the `v8_handles_paper`
directory and execute `make` (if on *BSD, you will need to use `gmake`). This
will build a file `v8_handles_paper.pdf` which should be a version of the paper
with your data in.

