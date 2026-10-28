/* The micro potato server: serves /index.html on port 80, one request at a
 * time, and 404 for anything but / and /index.html. */
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static char *read_page(const char *path, long *size) {
    FILE *file = fopen(path, "rb");
    if (!file || fseek(file, 0, SEEK_END) != 0 || (*size = ftell(file)) < 0) {
        perror(path);
        exit(1);
    }
    rewind(file);
    char *page = malloc(*size);
    if (!page || fread(page, 1, *size, file) != (size_t)*size) {
        perror(path);
        exit(1);
    }
    fclose(file);
    return page;
}

static void send_all(int fd, const char *data, size_t length) {
    while (length > 0) {
        ssize_t sent = send(fd, data, length, 0);
        if (sent <= 0) return;
        data += sent;
        length -= sent;
    }
}

int main(void) {
    long size;
    char *page = read_page("/index.html", &size);
    /* IPv4 only: OSv has no IPv6 sockets. */
    int server = socket(AF_INET, SOCK_STREAM, 0);
    int yes = 1;
    setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof yes);
    struct sockaddr_in address = { .sin_family = AF_INET, .sin_port = htons(80), .sin_addr.s_addr = htonl(INADDR_ANY) };
    if (server < 0 || bind(server, (struct sockaddr *)&address, sizeof address) != 0 || listen(server, 16) != 0) {
        perror("port 80");
        return 1;
    }
    printf("micro-potato: serving the Potato Operations Center on port 80\n");
    fflush(stdout);
    for (;;) {
        int client = accept(server, NULL, NULL);
        if (client < 0) continue;
        char request[2048];
        ssize_t got = recv(client, request, sizeof request - 1, 0);
        if (got > 0) {
            request[got] = '\0';
            char method[8] = "", target[256] = "";
            sscanf(request, "%7s %255s", method, target);
            int head = strcmp(method, "HEAD") == 0;
            char header[160];
            if ((head || strcmp(method, "GET") == 0) && (strcmp(target, "/") == 0 || strcmp(target, "/index.html") == 0)) {
                int length = snprintf(header, sizeof header,
                    "HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: %ld\r\n\r\n", size);
                send_all(client, header, length);
                if (!head) send_all(client, page, size);
            } else {
                static const char missing[] = "HTTP/1.0 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 10\r\n\r\nNot found\n";
                send_all(client, missing, head ? strlen(missing) - 10 : strlen(missing));
            }
        }
        close(client);
    }
}
