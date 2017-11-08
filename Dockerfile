FROM alpine:latest

RUN apk add --update grep bash py-pip python3-dev postgresql-dev gcc musl-dev supervisor curl openssl ca-certificates wget
RUN update-ca-certificates
RUN mkdir -p /srv/ip-reputation
WORKDIR /srv/ip-reputation

# We first add the requirements, so that we can install the python dependencies
# This way, we use the docker layers more efficiently
ADD requirements/ requirements/
ADD requirements.txt .

# Then we download the python requirements
RUN pip3 install -r requirements.txt && pip install supervisor
# And finally, we add the application source code
ADD . /srv/ip-reputation

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
