#include <stdio.h>
#include <string.h>
#include "cmd.h"

int main(int argc, char* argv[]) {
	if (argc <= 1) {
		printf("Use 'ehconsole --help' to see options\n");
		return 1;
	}

	if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0) {
		help();
		return 1;
	}

	return 1;
}
