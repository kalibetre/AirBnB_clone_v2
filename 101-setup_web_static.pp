# Installs and Configures an nginx web server
exec { 'update':
    command => '/usr/bin/env apt-get -y update',
}

package { 'nginx' :
  ensure     => installed,
  require    => Exec['update']
}

file { '/data/web_static/shared/':
  ensure     => 'directory',
  require    => Package['nginx']
}

file { '/data/web_static/releases/test/':
  ensure => 'directory',
  require    => File['/data/web_static/shared/']
}

file { 'Configure index.html':
  path       => '/data/web_static/releases/test/index.html',
  ensure     => present,
  content    => 'ALX SE School',
  require    => File['/data/web_static/releases/test/']
}

file_line { 'Customer Header':
  path       => '/etc/nginx/sites-available/default',
  ensure     => present,
  after      => 'server_name _;',
  line       => "\tadd_header X-Served-By ${hostname};",
  require    => Package['nginx']
}

file { '/data/':
  ensure => 'directory',
  owner => 'ubuntu',
  group => 'ubuntu',
  require    => File['Configure index.html']
}

file { '/data/web_static/current',
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  require    => File['/data/web_static/releases/test/']
}

file_line { 'Custom Location':
  path       => '/etc/nginx/sites-available/default',
  ensure     => present,
  after      => 'server_name _;',
  line       => "\\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n",
  require    => [Package['nginx'], File['/data/web_static/current']]
}

service { 'nginx' :
  ensure     => running,
  require    => [File_line['Custom Location'], File_line['Customer Header']]
}
