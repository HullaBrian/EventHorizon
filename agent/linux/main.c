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
#include "monitor.h"

int sockfd = 0, syslogfd = 0;

void clean_up(int signum) {
    printf("\n[+] Cleaning up...");

    close(sockfd);
    close(syslogfd);

    printf("Done!\n");
    exit_requested_main = 1;
}

int main(int argc, char* argv[]) {
    if (argc == 1) {
        printf("Invalid usage - please provide the path to the logging location configuration files\n");
        return -1;
    }

    if (signal(SIGINT, clean_up) == SIG_ERR) {
        perror("Failed to set up SIGINT handler");
        return EXIT_FAILURE;
    }

    char beacon[] = "Success!";
    // char HOST[] = LHOST;
    int n = 0;
    char buffer[1024];
    struct sockaddr_in serv_addr;

    memset(buffer, '\0', sizeof(buffer));

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        printf("\n Error : Could not create socket \n");
        return 1;
    }

    // serv_addr.sin_family = AF_INET;
    // serv_addr.sin_port = htons(PORT);
    // serv_addr.sin_addr.s_addr = INADDR_ANY;
    // printf("[+] Attempting to connect to remote server at %s:%d...", HOST, PORT);
    // fflush(stdout);

    // while (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
    //     sleep(1);
    //     printf(".");
    //     fflush(stdout);
    // }
    
    printf("Sending beacon...");
    fflush(stdout);
    sendto(sockfd, (const char *)beacon, strlen(beacon), MSG_CONFIRM, (const struct sockaddr*)&serv_addr, sizeof(serv_addr));
    printf("Done!\n");

    syslogfd = collect_syslog();

    // printf("[+] Setting up log monitoring...\n");
    // monitor(argv[1]);

    while (!exit_requested_main && (n = read(syslogfd, buffer, 1024)) > 0) {
        printf("[+] [SYSLOG]: %s\n", buffer);
    }

    if (n < 0) {
        printf("\n Error reading from socket! Was the connection closed? \n");
        return -1;
    }

    printf("Connection closed. Exiting...\n");
    return 0;
}