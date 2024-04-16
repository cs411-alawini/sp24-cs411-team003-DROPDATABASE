#include <stdio.h>

#include "mongoose.h"

#define PORT 1145;

static struct mg_mgr mgr;

void server_fn(struct mg_connection *c, int ev, void *ev_data)
{
    if (ev == MG_EV_HTTP_MSG)
    {
        struct mg_http_message *hm = (struct mg_http_message *)ev_data;
        struct mg_http_serve_opts opts = {.root_dir = "../", .page404 = "../index.html"};

        char uri[hm->uri.len + 1];
        strncpy(uri, hm->uri.ptr, hm->uri.len);
        uri[hm->uri.len] = '\0';

        printf("request: %s\n", uri);

        mg_http_serve_dir(c, ev_data, &opts);
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("usage: %s <PORT>", argv[0]);
        return 0;
    }

    char server_addr[32];

    sprintf(server_addr, "http://0.0.0.0:%d", atoi(argv[1]));
    mg_mgr_init(&mgr);

    if (!mg_http_listen(&mgr, server_addr, (mg_event_handler_t)server_fn, NULL))
        printf("can't listen on port %d", atoi(argv[1]));

    for (;;)
        mg_mgr_poll(&mgr, 1000); // Infinite event loop

    return 0;
}