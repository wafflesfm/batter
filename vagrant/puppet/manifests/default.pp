#set up defaults

Exec { path => '/usr/bin:/bin:/usr/sbin:/sbin' }
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
  ensure  => latest,
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


#add/setup virtualenvwrapper to auto start and add a tmux config that acts more like screen

file { '.bash_aliases': 
  path    => '/home/vagrant/.bash_aliases',
  source  => '/vagrant/files/bash_aliases',
  require => Package['virtualenvwrapper']
}

file { '.tmux.conf':
  path    => '/home/vagrant/.tmux.conf',
  source  => '/vagrant/files/tmux.conf',
  require => Package['tmux']
}

exec { 'create virtualenv': 
  command => "/bin/bash -c 'source /usr/local/bin/virtualenvwrapper.sh; mkvirtualenv batter'",
}

exec { 'install packages': 
  command => '/bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh; workon batter; /home/vagrant/.virtualenvs/batter/bin/pip install -r requirements.txt"',
  cwd     => '/home/vagrant/batter',
  require => Exec['create virtualenv'],
}