#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h> 
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

volatile sig_atomic_t exit_requested_main = 0;

#include "syslog_aggregator.h"
// #include "monitor.h"

int sockfd = 0, syslogfd = 0;

void clean_up(int signum) {
    printf("\n[+] Cleaning up...");

    close(sockfd);
    close(syslogfd);

    printf("Done!\n");
    exit_requested_main = 1;
}

int main(int argc, char* argv[]) {
    if (signal(SIGINT, clean_up) == SIG_ERR) {
        perror("Failed to set up SIGINT handler");
        return EXIT_FAILURE;
    }

    // char HOST[] = LHOST;
    int n = 0;
    char buffer[1024];
    struct sockaddr_in serv_addr;

    memset(buffer, '\0', sizeof(buffer));

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\nError : Could not create socket \n");
        return 1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    printf("[+] Attempting to connect to remote server at %s:%d...", LHOST, PORT);
    fflush(stdout);

    while (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        sleep(1);
        printf(".");
        fflush(stdout);
    }
    printf("Done!\n");

    syslogfd = collect_syslog();

    while (!exit_requested_main && (n = read(syslogfd, buffer, 1024)) > 0) {
        printf("[+] [SYSLOG]: %s\n", buffer);
        write(sockfd, buffer, sizeof(buffer));
    }

    if (n < 0) {
        printf("\nError reading from socket! Was the connection closed? \n");
        return -1;
    }

    printf("Connection closed. Exiting...\n");
    return 0;
}