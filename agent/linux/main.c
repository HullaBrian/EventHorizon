#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>

int main(int argc, char* argv[]) {
    int sockD = socket(AF_INET, SOCK_STREAM, 0);

    /*
    This isn't in a usable state *yet*
    */

    struct sockaddr_in servAddr;
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(PORT);
    servAddr.sin_addr.s_addr = INADDR_ANY;

    int connectStatus = connect(sockD, (struct sockaddr*)&servAddr, sizeof(servAddr));
    printf("");
    if (connectStatus == -1) {
        printf("Error connecting to server!\n");
        return -1;
    }
    
    char strData[255];
    recv(sockD, strData, sizeof(strData), 0);
    printf("Message, %s\n", strData);

    return 0;
}