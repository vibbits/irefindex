.PHONY: all clean flextest pytest

CC = gcc
CFLAGS = -O2 -Wall
LDLIBS = -lfl
LFLAGS = -Ca
LEX = flex

all: species species.py

clean:
	rm -f species species.c species.l species.py

species.l: flex.j2
	./scan-gen.py -t $< > $@

species.c: species.l

species: species.c

flextest: species
	./species example.txt

species.py: python.j2
	./scan-gen.py -t $< > $@
	chmod 755 $@

pytest: species.py
	./species.py example.txt

