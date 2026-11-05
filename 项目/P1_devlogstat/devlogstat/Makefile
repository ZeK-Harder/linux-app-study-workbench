CC     = gcc
CFLAGS = -Wall -Wextra -g -O0 -std=c11
TARGET = devlogstat

all: $(TARGET)

$(TARGET): src/main.c
	$(CC) $(CFLAGS) -o $@ $<

run: $(TARGET)
	./$(TARGET)

debug: $(TARGET)
	gdb ./$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all run debug clean
