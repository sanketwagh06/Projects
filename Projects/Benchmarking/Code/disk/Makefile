INSTALLDIR=./bin

CC = gcc

all: disk

disk:
	$(info Compiling DISK Benchmark)
	$(CC) diskbenchmark.c -lpthread -o diskbenchmark

run: disk
	$(info Running DISK Benchmark)
	./diskbenchmark
	
clean:
	rm diskbenchmark
