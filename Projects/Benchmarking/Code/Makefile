CC = gcc

all: cpuprog 

cpuprog:
	$(info In toplevel makefile)
	cd cpu ; make
	cd memory ; make
	cd disk ; make
gpuprog:
	$(info Will make GPU here, nvcc required)
	cd gpu ; make

runcpu:
	$(info running cpu)
	cd cpu ; make run
	cd memory ; make run
	cd disk ; make run
rungpu:
	$(info running gpu)
	cd gpu ; make run

clean:
	cd cpu ; make clean
	cd memory ; make clean
	cd disk ; make clean
	cd gpu ; make clean
