# Installs and Configures an nginx web server
exec { 'update':
  command => '/usr/bin/env apt-get -y update',
}

package { 'nginx' :
  ensure  => installed,
  require => Exec['update']
}

exec { 'create shared':
  command => '/usr/bin/env mkdir -p /data/web_static/shared'
}

exec { 'create test':
  command => '/usr/bin/env mkdir -p /data/web_static/releases/test',
  require => Exec['create shared']
}

exec { 'permission':
  command => '/usr/bin/env chown -R ubuntu:ubuntu /data/',
  require => File['Configure index.html']
}

file { 'Configure index.html':
  path       => '/data/web_static/releases/test/index.html',
  ensure     => present,
  content    => 'ALX SE School',
  owner      => 'ubuntu',
  group      => 'ubuntu',
  require    => Exec['create test']
}

exec { 'Custom Header':
  command => '/usr/bin/env sudo sed -i "/server_name _;/ a\\\tadd_header X-Served-By \$hostname;" /etc/nginx/sites-available/default',
  require    => Package['nginx']
}

file { 'create symlink':
  ensure     => 'link',
  path       => '/data/web_static/current',
  target     => '/data/web_static/releases/test/',
  owner      => 'ubuntu',
  group      => 'ubuntu',
  replace    => true,
  require    => File['Configure index.html']
}

exec { 'Custom Location':
  command => '/usr/bin/env sed -i "/server_name _;/ a\\\tlocation /hbnb_static\/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t\tindex index.html;\n\t}\n" /etc/nginx/sites-available/default',
  require => [Package['nginx'], File['create symlink']]
}

exec { 'nginx restart':
  command => '/usr/bin/env service nginx reload',
  require => Exec['Custom Location']
}
