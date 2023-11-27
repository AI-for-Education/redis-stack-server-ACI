FROM redis/redis-stack:latest 

USER root
RUN apt-get update && DEBIAN_FRONTEND=“noninteractive” apt-get install -y --no-install-recommends \
    nginx \
    ca-certificates \
    apache2-utils \
    certbot \
    python3-certbot-nginx \
    sudo \
    cifs-utils \
    && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install cron

RUN mkdir /opt/redis_stack
RUN chmod -R 777 /opt/redis_stack
WORKDIR /opt/redis_stack

RUN useradd redis
USER redis
COPY run.sh ./run.sh
COPY redis.conf /etc/redis/redis.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY refresh_cert.sh refresh_cert.sh

ENV PORT=6379
EXPOSE 6379
EXPOSE 6381

ARG REDIS_KEY
ENV REDISCLI_AUTH=${REDIS_KEY}

USER root
RUN chmod a+x run.sh
RUN chmod a+x refresh_cert.sh
RUN touch /var/log/cron.log
RUN (crontab -l ; echo "0 12 12 * * /opt/redis_stack/refresh_cert.sh" | crontab)

CMD ["./run.sh"]