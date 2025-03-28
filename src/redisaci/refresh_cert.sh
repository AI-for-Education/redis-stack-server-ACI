#! /bin/bash
/usr/bin/certbot renew --quiet &&
tar -cpzf /mnt/data/letsencrypt/etc.tar.gz -C / etc/letsencrypt/ &&
CERT_FILE=$(redis-cli -p 6381 --tls --raw config get tls-cert-file | tail -n1) &&
KEY_FILE=$(redis-cli -p 6381 --tls --raw config get tls-key-file | tail -n1) &&
echo $CERT_FILE &&
echo $KEY_FILE &&
redis-cli -p 6381 --tls config set tls-cert-file ${CERT_FILE} tls-key-file ${KEY_FILE}