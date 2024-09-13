#!/usr/bin/bash

cd /opt/blog.iscsc.fr
docker compose run --rm certbot renew
docker compose stop blog
docker compose up -d blog
