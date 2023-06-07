#!/bin/bash
#SBATCH -p wzhcexclu06
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mem=16000

srun sleep 10 && echo sleep-10-done
srun sleep 11 && echo sleep-11-done
srun sleep 12 && echo sleep-12-done
srun sleep 13 && echo sleep-13-done
srun sleep 14 && echo sleep-14-done
srun sleep 15 && echo sleep-15-done
wait