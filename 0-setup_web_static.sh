#!/usr/bin/env bash
# Sets up the web static pages deployment

apt-get -y update && apt-get -y install nginx

mkdir -p /data/web_static/shared/ /data/web_static/releases/test/

{
echo -e "\
<html>
  <head>
  </head>
  <body>
    ALX SE School
  </body>
</html>
"
} > /data/web_static/releases/test/index.html

ln -sfn /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

LOC_STATIC="\\\tlocation /hbnb_static\/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t\tindex index.html;\n\t}\n"
sed -i "/server_name _;/ a$LOC_STATIC" /etc/nginx/sites-available/default

service nginx restart
