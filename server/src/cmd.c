#include <stdio.h>
#include "cmd.h"

void help() {
	printf("Usage: ehconsole [OPTIONS]...\n\n");
	printf("Options:\n");
	printf("-h   --help            Prints this help menu\n");
	printf("-l   --listen  <port>  Listen on a specific port\n");
}
