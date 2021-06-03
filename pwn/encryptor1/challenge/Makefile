CC=gcc
CFLAGS=-Wall -Wextra -pedantic -no-pie -Wl,-z,noexecstack
LDFLAGS=
SOURCES=encryptor.c
OBJECTS=$(SOURCES:.c=.o)
BINARY=encryptor

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
