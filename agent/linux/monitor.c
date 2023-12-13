#include <dirent.h> 
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <sys/inotify.h>

#include "monitor.h"

int inotify_fd = -1;
FILE* log_f;
int monitored_fds[10];
volatile sig_atomic_t exit_requested = 0;

void monitor_file(const char *filename) {
    int watch_desc = inotify_add_watch(inotify_fd, filename, IN_MODIFY);

    int i = 0;
    for (int i = 0; i < 9 || monitored_fds[i] != -1; i++) {}
    if (monitored_fds[9] == -1 || i < 9) {
        monitored_fds[i] = watch_desc;
    }

    if (watch_desc == -1) {
        printf("\n[-] Error: Could not add watch on file '%s'\n", filename);
        perror("inotify_add_watch");
        exit(EXIT_FAILURE);
    }
}

void clean_up_main(int signum) {
    printf("\n[+] Cleaning up...");
    fflush(stdout);

    close(inotify_fd);
    for (int i = 0; i < 10; i++) {
        inotify_rm_watch(inotify_fd, monitored_fds[i]);
    }
    fclose(log_f);

    printf("Done!\n");
    fflush(stdout);

    exit_requested = 1;
}

int monitor(char* logging_location) {
    if (signal(SIGINT, clean_up_main) == SIG_ERR) {
        perror("Failed to set up SIGINT handler");
        return EXIT_FAILURE;
    }

    inotify_fd = inotify_init();
    for (int i = 0; i < 10; i++) { monitored_fds[i] = -1; }  // default values

    if (inotify_fd == -1) {
        perror("inotify_init");
        return EXIT_FAILURE;
    }

    log_f = fopen(logging_location, "r");
    char line[20];

    if (log_f == NULL) {
        printf("[-] Error: Could not open '%s'!\n", logging_location);
        return -1;
    }

    while (fgets(line, 20, log_f) != NULL) {
        printf("[+] Initializing monitoring on '%s'...", line);
        fflush(stdout);
        monitor_file(line);
        printf("Done!\n");
        fflush(stdout);
    }

    char buffer[BUF_LEN];

    printf("[+] Monitoring initialized! Waiting for modifications...\n");
    while (!exit_requested) {
        ssize_t length = read(inotify_fd, buffer, BUF_LEN);
        if (exit_requested) {
            break;
        }
        if (length == -1) {
            perror("read");
            break;
        }

        for (ssize_t i = 0; i < length;) {
            struct inotify_event *event = (struct inotify_event *)&buffer[i];

            printf("[+] Something happened to '%s'\n", event->name);

            i += EVENT_SIZE + event->len;
        }
    }

    return EXIT_SUCCESS;
}