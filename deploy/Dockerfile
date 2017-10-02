FROM alpine:latest

RUN mkdir -p /srv/ip-reputation
ADD . /srv/ip-reputation
WORKDIR /srv/ip-reputation

RUN apk add --update bash py-pip python3-dev postgresql-dev gcc musl-dev supervisor curl openssl ca-certificates wget
RUN update-ca-certificates
RUN pip3 install -r requirements.txt && pip install supervisor
RUN mkdir -p /var/log && \
    mkdir -p /etc/supervisor && \
    mkdir -p /usr/local/bin/ && \
    mv deploy/supervisor.conf /etc/ && \
    mv deploy/exit-event-listener /usr/local/bin/ && \
    cat deploy/crontab >> /etc/crontabs/root

CMD crond && supervisord -c /etc/supervisor.conf
