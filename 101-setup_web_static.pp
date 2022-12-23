# Installs and Configures an nginx web server
exec { 'update':
  command => '/usr/bin/env apt-get -y update',
}

package { 'nginx' :
  ensure  => installed,
  require => Exec['update']
}

exec { 'create shared':
  command => 'mkdir -p /data/web_static/shared'
}

exec { 'create test':
  command => 'mkdir -p /data/web_static/releases/test',
  require => Exec['create shared']
}

file { 'permission':
  path => '/data',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
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

file_line { 'Customer Header':
  path       => '/etc/nginx/sites-available/default',
  ensure     => present,
  after      => 'server_name _;',
  line       => "\tadd_header X-Served-By ${hostname};",
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

file_line { 'Custom Location':
  path       => '/etc/nginx/sites-available/default',
  ensure     => present,
  after      => 'server_name _;',
  line       => "\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n",
  require    => [Package['nginx'], File['create symlink']]
}

service { 'nginx' :
  ensure     => running,
}

exec { 'nginx_reload':
  path       => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  user       => 'root',
  command    => 'service nginx reload',
  require    => File_line['Custom Location'],
}
