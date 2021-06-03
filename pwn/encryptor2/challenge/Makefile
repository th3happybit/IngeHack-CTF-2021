CC=gcc
CFLAGS=-Wall -Wextra -pedantic -Wl,-z,noexecstack
LDFLAGS=
SOURCES=encryptor2.c
OBJECTS=$(SOURCES:.c=.o)
BINARY=encryptor2

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
