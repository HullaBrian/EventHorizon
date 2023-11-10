server: build/server/main.o 
	@echo "Building server..."

build/server/main.o: server/src/main.c
	gcc -Wall -c server/src/main.c -o build/server/main.o

agent: build/agent/main.o
	@echo "Building agent..."

build/agent/main.o: agent/src/main.c
	gcc -Wall -c agent/src/main.c -o build/agent/main.o
