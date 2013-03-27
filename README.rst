========================
Batter
========================

It makes Waffles.

To develop on this project follow these steps:

#. Create your working environment
#. Install dependencies
#. Update the database schema
#. Get coding!

Working Environment
===================

First, make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv --distribute venv
    $ source venv/bin/activate

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

Installation of Dependencies
============================

    $ pip install -r requirements/local.txt

Updating the Database Schema
============================

    $ python batter/manage.py syncdb
    $ python batter/manage.py migrate

Get Coding!
===========

We use git-flow (https://github.com/nvie/gitflow) for our development model. 
Read this article - http://qq.is/article/git-flow-on-github - for how to use
git-flow in tandem with GitHub pull requests.
