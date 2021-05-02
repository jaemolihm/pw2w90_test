#!/bin/bash
#SBATCH --partition=fast      # select partition (normal or fast)
#SBATCH --time=02:00:00         # set time limit in HH:MM:SS
#SBATCH --nodes=1               # number of nodes
#SBATCH --ntasks=16             # number of processes (for MPI)
#SBATCH --cpus-per-task=1       # OMP_NUM_THREADS (for openMP)
#SBATCH --job-name=diam.lib    # job name
#SBATCH --output="error.%x"    # standard output and error are redirected to
				# <job name>_<job ID>.out
# for OpenMP jobs
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
# load modules
module purge
module load intel/2019
# quantum espresso executable
QE=/group2/jmlim/dipole/q-e/bin
WANN=/group2/jmlim/program/wannier90/wannier90.x

# # run parallel
# srun -n 16 $QE/pw.x -nk 4 -in scf.in > scf.out
# srun -n 16 $QE/pw.x -nk 4 -in nscf.in > nscf.out

rm diam.chk diam.chk.fmt

srun -n 1 $QE/pw2wannier90.x -nk 1 -in pw2wan.in > pw2wan.out
w90chk2chk.x -u2f diam

