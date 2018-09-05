// C HTTP request client for sending simple GET requests
// adapted from https://stackoverflow.com/questions/22077802/simple-c-example-of-doing-an-http-post-and-consuming-the-response

#include <stdio.h> /* printf, sprintf */
#include <stdlib.h> /* exit */
#include <stdbool.h>
#include <unistd.h> /* read, write, close */
#include <string.h> /* memcpy, memset */
#include <sys/socket.h> /* socket, connect */
#include <netinet/in.h> /* struct sockaddr_in, struct sockaddr */
#include <netdb.h> /* struct hostent, gethostbyname */
#include <time.h>

void error(const char *msg);
void printDuration(int duration);

int main(int argc,char *argv[])
{
    /* first what are we going to send and where are we going to send it? */
    int portno =        8081;
    char *host =        "172.20.10.2";
    char *message_fmt = "%s /%s HTTP/1.1\r\n\r\n";

    struct hostent *server;
    struct sockaddr_in serv_addr;
    int sockfd, bytes, sent, received, total, repeat;
    char message[1024],response[1001000];

    if (argc != 4) { puts("Parameters: <request_type(in CAPS)> <URI> <repeat>"); exit(0); }

    /* fill in the parameters */
    sprintf(message,message_fmt,argv[1],argv[2]);
    if (sscanf(argv[3], "%i", &repeat) != 1) {
		fprintf(stderr, "error - repeat val (third arg) is not an integer");
	}
 	printf("repeat : %d\n",repeat);
	printf("Request:\n%s\n",message);

    /* lookup the ip address */
    server = gethostbyname(host);
    if (server == NULL) error("ERROR, no such host");

    /* fill in the structure */
    memset(&serv_addr,0,sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(portno);
    memcpy(&serv_addr.sin_addr.s_addr,server->h_addr,server->h_length);

	time_t before, after;
	time(&before);
    for (size_t i = 0; i < repeat; i++) {
        /* create the socket */
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) error("ERROR opening socket");

        /* connect the socket */
        if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0) {
            error("ERROR connecting");
        }

        /* send the request */
        total = strlen(message);
        sent = 0;
        do {
            bytes = write(sockfd,message+sent,total-sent);
            if (bytes < 0)
                error("ERROR writing message to socket");
            if (bytes == 0)
                break;
            sent+=bytes;
        } while (sent < total);

        /* receive the response */
        memset(response,0,sizeof(response));
        total = sizeof(response)-1;
        received = 0;
        do {
            bytes = read(sockfd,response+received,total-received);
            if (bytes < 0)
                error("ERROR reading response from socket");
            if (bytes == 0)
                break;
            received+=bytes;
        } while (received < total);

        if (received == total)
            error("ERROR storing complete response from socket");

        /* process response */
        printf("Response:\n%s\n",response);

        /* close the socket */
        close(sockfd);
    }
    time(&after);

	printf("Execution time: %d",(int)(after-before));

    return 0;
}

void error(const char *msg) {
    printf("%s\n", msg);
    exit(0);
}
