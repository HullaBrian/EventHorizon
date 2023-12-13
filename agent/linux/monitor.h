#ifndef MONITOR_H
#define MONITOR_H

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define BUF_LEN     (1024 * (EVENT_SIZE + 16))

void monitor_file(const char *filename);
void clean_up(int signum);
int monitor();

#endif