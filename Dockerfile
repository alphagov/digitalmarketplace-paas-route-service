FROM nginx:1.19.6

ENV APP_DIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    python3.7 python3-setuptools python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir supervisor==4.2.1 awscli awscli-cwlogs && \
    aws configure set plugins.cwlogs cwlogs && \
    mkdir -p ${APP_DIR} && \
    mkdir -p /etc/nginx/sites-available && \
    mkdir -p /etc/nginx/sites-enabled && \
    mkdir -p /usr/share/nginx/html && \
    mkdir -p /var/log/digitalmarketplace && \
    rm -f /etc/nginx/nginx.conf /etc/nginx/sites-enabled/*

COPY requirements.txt ${APP_DIR}
RUN pip3 install -r ${APP_DIR}/requirements.txt

COPY static_files/* /usr/share/nginx/html/

COPY awslogs/awslogs.conf /etc/awslogs.conf
COPY awslogs/run.sh /awslogs.sh

COPY supervisord.conf /etc/supervisord.conf

COPY nginx.sh /nginx.sh

COPY templates/ ${APP_DIR}/templates/
COPY scripts/ ${APP_DIR}/scripts/

CMD ["supervisord", "--configuration", "/etc/supervisord.conf"]
