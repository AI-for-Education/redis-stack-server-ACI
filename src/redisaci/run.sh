#!/bin/bash

tar -xzf /mnt/data/letsencrypt/etc.tar.gz -C / &&
nginx -t &&
service nginx start &&
cron &&

redis-stack-server /etc/redis/redis.conf --dir /mnt/data/redis
# while true; do redis-cli -h localhost -p 6379 ping; sleep 5; done