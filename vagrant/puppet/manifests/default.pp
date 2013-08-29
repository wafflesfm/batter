#set up defaults

Exec { path => '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin/' }
exec { 'echo this works': }

#set up updated apt-get repos

group { 'puppet': ensure => 'present' }

exec { 'apt-get update':
  command => '/usr/bin/apt-get update'
}


#install system packages that some python libs depend on

package { 'python-dev':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'python-virtualenv':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'redis-server':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'libtag1-dev':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'git':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'zlib1g-dev':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'libxml2-dev':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'libxslt-dev':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'vim':
  ensure  => present,
  require => Exec['apt-get update']
}

package { 'virtualenvwrapper':
  ensure   => latest,
  provider => pip,
}

package { 'tmux':
  ensure  => present,
  require => Exec['apt-get update']
}

service { 'redis-server':
  ensure  => running,
  require => Package['redis-server']
}


# add/setup virtualenvwrapper to auto start

file { '.bash_aliases':
  path    => '/home/vagrant/.bash_aliases',
  source  => '/vagrant/files/bash_aliases',
}

# add a tmux config that acts more like screen

file { '.tmux.conf':
  path    => '/home/vagrant/.tmux.conf',
  source  => '/vagrant/files/tmux.conf',
  require => Package['tmux']
}

file { '/vagrant/files/install_venv.sh':
  ensure  => 'present',
  mode    => '0777',
  source  => '/vagrant/files/install_venv.sh',
}

exec { '/vagrant/files/install_venv.sh':
  require   => [
    Package['python-virtualenv'],
    Package['virtualenvwrapper'],
    File['.bash_aliases'],
    File['/vagrant/files/install_venv.sh'],
  ],
  logoutput => 'on_failure'
}
