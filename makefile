gravity: build/agent/main.o
	@echo "Building agent..."
	gcc build/agent/main.o -o gravity

build/agent/main.o: agent/linux/main.c
	gcc -Wall -c agent/linux/main.c -o build/agent/main.o -D PORT=$(PORT) -D LHOST=\"$(LHOST)\"

clean:
	rm -f build/agent/*.o
	rm -f gravity