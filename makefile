server: build/server/main.o build/server/cmd.o
	@echo "Building server..."
	gcc build/server/main.o build/server/cmd.o -o ehconsole

build/server/main.o: server/src/main.c server/src/cmd.h
	gcc -Wall -c server/src/main.c -o build/server/main.o

build/server/cmd.o: server/src/cmd.c server/src/cmd.h
	gcc -Wall -c server/src/cmd.c -o build/server/cmd.o

agent: build/agent/main.o
	@echo "Building agent..."

build/agent/main.o: agent/src/main.c
	gcc -Wall -c agent/src/main.c -o build/agent/main.o
