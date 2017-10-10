FROM alpine:latest

RUN apk add --update bash py-pip python3-dev postgresql-dev gcc musl-dev supervisor curl openssl ca-certificates wget
RUN update-ca-certificates
RUN mkdir -p /srv/ip-reputation
WORKDIR /srv/ip-reputation

ADD requirements/ requirements/
ADD requirements.txt .
RUN pip3 install -r requirements.txt && pip install supervisor
ADD . .

RUN mkdir -p /var/log && \
    touch /var/log/reputation-rbl.log /var/log/spamhaus-bl.log /var/log/fetch_ips.log && \
    mkdir -p /etc/supervisor && \
    mkdir -p /usr/local/bin/ && \
    mv deploy/supervisor.conf /etc/ && \
    mv deploy/exit-event-listener /usr/local/bin/ && \
    cat deploy/crontab >> /etc/crontabs/ip-reputation
RUN adduser -D -H ip-reputation
RUN chown ip-reputation /srv/ip-reputation -R && chown ip-reputation /var/log/*.log 

CMD crond && \ 
    { tail -f /var/log/*.log & \
      supervisord -c /etc/supervisor.conf ; }
