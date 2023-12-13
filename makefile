gravity: build/agent/main.o build/agent/monitor.o build/agent/syslog_aggregator.o
	@echo "Building agent..."
	gcc build/agent/main.o build/agent/monitor.o build/agent/syslog_aggregator.o -o gravity

build/agent/main.o: agent/linux/main.c agent/linux/monitor.h agent/linux/syslog_aggregator.h
	gcc -Wall -c agent/linux/main.c -o build/agent/main.o -D PORT=$(PORT) -D LHOST=\"$(LHOST)\"

build/agent/monitor.o: agent/linux/monitor.c agent/linux/monitor.h
	gcc -Wall -c agent/linux/monitor.c -o build/agent/monitor.o

build/agent/syslog_aggregator.o: agent/linux/syslog_aggregator.c agent/linux/syslog_aggregator.c
	gcc -Wall -c agent/linux/syslog_aggregator.c -o build/agent/syslog_aggregator.o -D PORT=$(PORT)+1

clean:
	rm -f build/agent/*.o
	rm -f gravity