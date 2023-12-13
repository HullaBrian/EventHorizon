gravity: build/agent/main.o build/agent/monitor.o
	@echo "Building agent..."
	gcc build/agent/main.o build/agent/monitor.o -o gravity

build/agent/main.o: agent/linux/main.c agent/linux/monitor.h
	gcc -Wall -c agent/linux/main.c -o build/agent/main.o -D PORT=$(PORT) -D LHOST=\"$(LHOST)\"

build/agent/monitor.o: agent/linux/monitor.c agent/linux/monitor.h
	gcc -Wall -c agent/linux/monitor.c -o build/agent/monitor.o

clean:
	rm -f build/agent/*.o
	rm -f gravity