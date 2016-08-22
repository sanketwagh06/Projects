INSTALLDIR=./bin

CC = gcc

all: cpu

cpu:
	$(info Compiling CPU Benchmark)
	$(CC) cpubenchmark.c -lpthread -o cpubenchmark

run: cpu
	$(info Running CPU Benchmark)
	./cpubenchmark
	
clean:
	rm cpubenchmark
