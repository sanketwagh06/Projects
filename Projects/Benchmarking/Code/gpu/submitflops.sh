#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -m n
#$ -pe mpich 1
#$ -S /bin/bash
#PBS -l walltime=00:05:00
./gpuflopsbench