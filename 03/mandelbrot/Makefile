# Compiler and Flags
CFLAGS = -std=gnu11 -Wall -Werror -Wextra
LDFLAGS = -lm

CC = gcc
OMP_FLAG = -fopenmp
OPT_FLAGS = -O3 -march=native

# Targets
APPS = mandelbrot
APPS_OPT = mandelbrot_opt
RUNS = 10

.PHONY: all clean run_benchmarks

all: $(APPS) $(APPS_OPT)

mandelbrot: mandelbrot.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

# Standard Compilation (-O0 by default)
%: %.c
	$(CC) $(OMP_FLAG) $< -o $@

# Optimized Compilation (-O3)
%_opt: %.c
	$(CC) $(OMP_FLAG) $(OPT_FLAGS) $< -o $@

# Simple benchmark helper for local testing
run_benchmarks: all
	@echo "Starting measurements ($(RUNS) per config)..."
	@echo "Threads,Program,Run,Time" > results.csv
	@for t in 1 2 4 8 12; do \
		export OMP_NUM_THREADS=$$t; \
		for app in $(APPS) $(APPS_OPT); do \
			for run in $$(seq 1 $(RUNS)); do \
				echo "  $$app  threads=$$t  run=$$run"; \
				tval=`./$$app | awk -F': ' '{print $$2}' | awk '{print $$1}'`; \
				echo "$$t,$$app,$$run,$$tval" >> results.csv; \
			done; \
		done; \
	done
	@echo "Measurements finished. Data saved in results.csv"

clean:
	rm -f $(APPS) $(APPS_OPT) results.csv