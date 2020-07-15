#!/bin/bash

exec /usr/local/bin/nginx-prometheus-exporter \
    -web.listen-address :9113 \
    -nginx.retries 3 \
    -nginx.scrape-uri http://127.0.0.1:9112/stub-status
