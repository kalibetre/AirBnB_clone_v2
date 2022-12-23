# Installs nginx and stuff like that
exec { '/usr/bin/env apt-get -y update' : }
-> exec { '/usr/bin/env apt-get -y install nginx' : }
-> exec { '/usr/bin/env sed -i "/listen \[::\]:80 default_server/ a\\\trewrite ^/redirect_me http://www.holbertonschool.com permanent;" /etc/nginx/sites-available/default' : }
-> exec { '/usr/bin/env sed -i "/listen \[::\]:80 default_server/ a\\\tadd_header X-Served-By \"\$HOSTNAME\";" /etc/nginx/sites-available/default' : }
-> exec { '/usr/bin/env sed -i "/redirect_me/ a\\\terror_page 404 /custom_404.html;" /etc/nginx/sites-available/default' : }
-> exec { '/usr/bin/env # echo "Ceci n\'est pas une page" > /var/www/html/custom_404.html' : }
-> exec { '/usr/bin/env service nginx start' : }
-> exec { '/usr/bin/env mkdir -p /data/web_static/releases/test/' : }
-> exec { '/usr/bin/env mkdir -p /data/web_static/shared/' : }
-> exec { '/usr/bin/env echo "Hello Holberton School!" > /data/web_static/releases/test/index.html' : }
-> exec { '/usr/bin/env ln -sf /data/web_static/releases/test/ /data/web_static/current' : }
-> exec { '/usr/bin/env sed -i "/^\tlocation \/ {$/ i\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n}" /etc/nginx/sites-available/default' : }
-> exec { '/usr/bin/env service nginx restart' : }
-> exec { '/usr/bin/env chown -R ubuntu:ubuntu /data/' : }
