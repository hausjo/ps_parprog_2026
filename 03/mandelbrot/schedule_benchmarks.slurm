#!/bin/bash

# Name of your job.
#SBATCH --job-name=mandelbrot_benchmark

# Send status information to this email address.
#SBATCH --mail-user=johannes.hausmann@student.uibk.ac.at

# Send an e-mail when the job has finished or failed.
#SBATCH --mail-type=END,FAIL

# Reserve 12 threads (cpus) not using hyperthreading here cause it will likely be slower and fake the benchmarks??
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
## #SBATCH --nodes=1
#SBATCH --mem-per-cpu=1G
#SBATCH --exclusive

module purge # reset the module space/cache/mem whatever
module load gcc/12.2.0-gcc-8.5.0-p4pe45v        

make clean
# make all
make run_benchmarks
