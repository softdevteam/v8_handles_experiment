.SUFFIXES: .tex

all:
	python process.py results

clean:
	rm -rf experimentstats.tex table_min.tex table_no_stack_compact.tex
