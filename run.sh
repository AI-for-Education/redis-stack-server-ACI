#!/bin/bash

tar -xzf /mnt/letsencrypt/etc.tar.gz -C / &&
nginx -t &&
service nginx start &&
cron &&

redis-stack-server /etc/redis/redis.conf
# while true; do redis-cli -h localhost -p 6379 ping; sleep 5; done