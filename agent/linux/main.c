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
#include <openssl/evp.h>
#include <openssl/aes.h>

volatile sig_atomic_t exit_requested_main = 0;

#include "syslog_aggregator.h"

int sockfd = 0, syslogfd = 0;

int encrypt(const unsigned char *key, const unsigned char *iv,
            const unsigned char *msg, size_t msg_len, unsigned char *out)
{
   /*
    * This assumes that key size is 32 bytes and the iv is 16 bytes.
    * For ciphertext stealing mode the length of the ciphertext "out" will be
    * the same size as the plaintext size "msg_len".
    * The "msg_len" can be any size >= 16.
    */
    int ret = 0, encrypt = 1, outlen, len;
    EVP_CIPHER_CTX *ctx = NULL;
    EVP_CIPHER *cipher = NULL;
    // OSSL_PARAM params[2];

    ctx = EVP_CIPHER_CTX_new();
    cipher = EVP_CIPHER_fetch(NULL, "AES-256-CTR", NULL);
    if (ctx == NULL || cipher == NULL)
        goto err;

    if (!EVP_CipherInit_ex2(ctx, cipher, key, iv, encrypt, NULL))
        goto err;

    if (!EVP_CipherUpdate(ctx, out, &outlen, msg, msg_len))
        goto err;
    if (!EVP_CipherFinal_ex(ctx, out + outlen, &len))
        goto err;
    ret = 1;
    
    err:
        EVP_CIPHER_free(cipher);
        EVP_CIPHER_CTX_free(ctx);
    return ret;
}

void clean_up(int signum) {
    printf("\n[+] Cleaning up...");

    close(sockfd);
    close(syslogfd);
    exit_requested_main = 1;

    printf("Done!\n");
}

int msleep(long tms)
{
    struct timespec ts;
    int ret;

    if (tms < 0)
    {
        errno = EINVAL;
        return -1;
    }

    ts.tv_sec = tms / 1000;
    ts.tv_nsec = (tms % 1000) * 1000000;

    do {
        ret = nanosleep(&ts, &ts);
    } while (ret && errno == EINTR);

    return ret;
}

int main(int argc, char* argv[]) {
    if (signal(SIGINT, clean_up) == SIG_ERR) {
        perror("Failed to set up SIGINT handler");
        return EXIT_FAILURE;
    }

    char HOST[] = LHOST;
    int n = 0;
    uint8_t buffer[1024];
    uint8_t e_buffer[1024];
    struct sockaddr_in serv_addr;
    uint8_t key[33] = KEY;  // KEY;
    uint8_t iv[] = IV;  // IV;
    uint8_t hello[33] = UUID;

    memset(buffer, '\0', 1024);
    memset(e_buffer, '\0', 1024);
    
    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\nError : Could not create socket \n");
        return 1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    printf("[+] Attempting to connect to remote server at %s:%d...", HOST, PORT);
    fflush(stdout);

    while (!exit_requested_main && connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        sleep(1);
        printf(".");
        fflush(stdout);
    }
    printf("Done!\n[+] Sending hello message...");
    write(sockfd, hello, sizeof(hello) - 1);
    printf("Done!\n");

    if (exit_requested_main){
        close(sockfd);
        return 1;
    }

    syslogfd = collect_syslog();

    // Not sure why, but sometimes the agent randomly exits after reading only a small amount of data
    // 
    // memset is called so much to try and fix an issue regarding the agent sending a bunch of random data
    // ..it doesn't work 100% of the time :(
    // TODO: FIX SEG FAULTS WHEN SENDING SIG TERMs
    while (!exit_requested_main) {
        memset(buffer, '\0', 1024);
        memset(e_buffer, '\0', 1024);
        n = read(syslogfd, buffer, 1024);

        if (exit_requested_main && n == 0) break;
        encrypt(key, iv, buffer, n, e_buffer);
        printf("[+] [SYSLOG] (%ld)~(%d): %s\n", sizeof(e_buffer), n, buffer);
        if (exit_requested_main && n == 0) break;
        write(sockfd, e_buffer, n);

        memset(buffer, '\0', 1024);
        memset(e_buffer, '\0', 1024);
        msleep(1);
    }

    if (n < 0) {
        printf("\nError reading from socket! Was the connection closed? \n");
        return -1;
    }

    printf("Connection closed. Exiting...\n");
    return 0;
}