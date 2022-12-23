#!/usr/bin/env bash
# Sets up the web static pages deployment

apt-get -y update && apt-get -y install nginx

mkdir -p /data/web_static/shared/ /data/web_static/releases/test/

echo "ALX SE School" > /data/web_static/releases/test/index.html

ln -sfn /data/web_static/releases/test/ /data/web_static/current

chown -hR ubuntu:ubuntu /data

sed -i "s/^\}$/\tlocation \/hbnb_static\/ \{\n\t\talias \/data\/web_static\/current\/\;\n\t\}\n\}/" /etc/nginx/sites-available/default

service nginx restart
