INSTALLDIR=./bin

CC = gcc

all: memory

memory:
	$(info Compiling Memory Benchmark)
	$(CC) memorybenchmark.c -lpthread -o memorybenchmark

run: memory
	$(info Running Memory Benchmark)
	./memorybenchmark
	
clean:
	rm memorybenchmark
