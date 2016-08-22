
The directory contains different programs for CPU and GPU benchmarking.

We have divided them into parts :

cpuprog :
CPU,Memory,Disk

gpuprog :
GPU

These can be run with makefile with below instructions.

The GPU prog will require nvcc installed, since it is written in CUDA C.

The benchmark for network is written in python. For that We have written shell script which needs to be run.
====
Instructions :
====

1. For CPU, Memory, Disk :

To Compile the cpuprog programs, run command : make cpuprog 
To Run the cpuprog programs, run command : make runcpu
====

2. For GPU :

To Compile the gpuprog programs, run command : make gpuprog 
To Run the gpuprog programs, run command : make rungpu
====

3. For Network :

Go to network directory.
Run command : ./scricpt.sh

