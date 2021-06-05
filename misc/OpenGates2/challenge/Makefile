CC=gcc
CFLAGS=-Wall -Wextra -ansi -pedantic -Wl,-z,noexecstack
LDFLAGS=-lcrypto
SOURCES=OpenGates.c
OBJECTS=$(SOURCES:.c=.o)
BINARY=OpenGates

.PHONY : clean

all: $(SOURCES) $(BINARY)

$(BINARY): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $@ $(LDFLAGS)

.o:
	$(CC) $(CFLAGS) $< -o $@

chall: all
	rm -f $(OBJECTS)

clean:
	rm -f $(BINARY) $(OBJECTS)
