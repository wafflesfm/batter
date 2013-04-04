Using Vagrant for development of Batter
=======================================

1. Install vagrant (http://vagrantup.com)
2. In this directory run `vagrant up`
3. Run `vagrant ssh`
4. Once you are ssh'd go ahead and run `workon batter` to activate the `venv`
5. You're good to go! `vagrant` automatically installed all the required python libs and system packages and mounted the projects code folder to a network share called `batter`. Happy Dev'ing!