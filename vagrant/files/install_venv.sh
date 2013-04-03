#!/bin/bash

. /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv batter 
/home/vagrant/.virtualenvs/batter/bin/pip install -r /home/vagrant/batter/requirements.txt

exit