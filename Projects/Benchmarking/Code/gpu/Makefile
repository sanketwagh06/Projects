INSTALLDIR=./bin

NVCC = nvcc
SUBMIT = qsub 

all: gpu

gpu:
	$(info Compiling GPU Benchmark)
	$(NVCC) gpuflopsbench.cu -lpthread -o gpuflopsbench
	$(NVCC) gpumembench.cu -lpthread -o gpumembench

run: gpu
	$(info Running GPU Benchmarks)
	$(info Running GPU FLOPS_IOPS Benchmark)
	$(SUBMIT) submitflops.sh
	$(info Running GPU Memory Benchmark)
	$(SUBMIT) submitmem.sh
clean:
	rm gpuflopsbench gpumembench
