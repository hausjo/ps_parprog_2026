# Compiler and Flags
CFLAGS = -std=gnu11 -Wall -Werror -Wextra

CC = gcc
OMP_FLAG = -fopenmp
OPT_FLAGS = -O3 -march=native

# Targets
APPS = false_sharing no_false_sharing
RUNS = 10
PROBLEM_SIZE = 100000000


.PHONY: all clean run_benchmarks

all: $(APPS)

false_sharing: false_sharing.c
	$(CC) $(CFLAGS) $(OMP_FLAG) $< -o $@

no_false_sharing: false_sharing_2.c
	$(CC) $(CFLAGS) $(OMP_FLAG) $< -o $@


# Benchmark
run_benchmarks: all
	@echo "Starting measurements ($(RUNS) per config)..."
	@echo "Threads,Affinity,Program,Run,Time" > results.csv
	@for affinity in "0-1-2-3-4-5" "0-1-2-6-7-8"; do \
		gomp_affinity=$$(echo $$affinity | tr '-' ','); \
		for app in $(APPS); do \
			for run in $$(seq 1 $(RUNS)); do \
				echo "  $$app  affinity=$$gomp_affinity  run=$$run"; \
				tval=$$(OMP_NUM_THREADS=6 GOMP_CPU_AFFINITY=$$gomp_affinity ./$$app $(PROBLEM_SIZE) | grep "Time" | awk -F': ' '{print $$2}' | awk '{print $$1}'); \
				echo "6,$$affinity,$$app,$$run,$$tval" >> results.csv; \
			done; \
		done; \
	done
	@echo "Measurements finished. Data saved in results.csv"

clean:
	rm -f $(APPS) results.csv

# inspect performance
run_perf: all
	@echo "Running perf stat analysis..."
	@for affinity in "0-1-2-3-4-5" "0-1-2-6-7-8"; do \
		gomp_affinity=$$(echo $$affinity | tr '-' ','); \
		for app in $(APPS); do \
			echo "=== $$app  affinity=$$gomp_affinity ==="; \
			OMP_NUM_THREADS=6 GOMP_CPU_AFFINITY=$$gomp_affinity \
				perf stat ./$$app $(PROBLEM_SIZE) 2>&1; \
		done; \
	done

run_perf_cache: all
	@echo "Running perf cache analysis..."
	@for affinity in "0-1-2-3-4-5" "0-1-2-6-7-8"; do \
		gomp_affinity=$$(echo $$affinity | tr '-' ','); \
		for app in $(APPS); do \
			echo "=== $$app  affinity=$$gomp_affinity ==="; \
			OMP_NUM_THREADS=6 GOMP_CPU_AFFINITY=$$gomp_affinity \
				perf stat \
				-e LLC-load-misses \
				-e LLC-store-misses \
				-e L1-dcache-load-misses \
				-e L1-dcache-store-misses \
				./$$app $(PROBLEM_SIZE) 2>&1; \
		done; \
	done