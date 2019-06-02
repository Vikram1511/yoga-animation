CC=g++ 

CFLAGS=-c -Wall

all: k2b

k2b: main.o kinectbvh.o catmull_rom.o vec_math.o
	$(CC) main.o kinectbvh.o catmull_rom.o vec_math.o

main.o: main.cpp 
	$(CC) $(CFLAGS) main.cpp

kinectbvh.o: kinectbvh.h
	$(CC) $(CFLAGS) kinectbvh.h

catmull_rom.o: catmull_rom.h
	$(CC) $(CFLAGS) catmull_rom.h

vec_math.o: vec_math.h
	$(CC) $(CFLAGS) vec_math.h


clean: 
	rm -rf *.o k2b