Batter
======

It makes Waffles (and other tasty things)!

[![Build Status](https://travis-ci.org/wafflesfm/batter.png?branch=develop)](https://travis-ci.org/wafflesfm/batter) [![Coverage Status](https://coveralls.io/repos/wafflesfm/batter/badge.png?branch=develop)](https://coveralls.io/r/wafflesfm/batter)

To develop on this project follow these steps:

1. Download the code
2. Vagrant up!
3. Create the database schema
4. Run Batter
5. Contribute changes!

Download the code
-----------------

You can get the most recent copy of Batter by cloning this repository:

    git clone git://github.com/wafflesfm/batter.git

which will copy all of Batter into a new folder called `batter`.

Vagrant up!
-----------

Vagrant is a way to create and configure lightweight, reproducible, and
portable development environments. We use it to keep the Batter runtime
in sync across our machines. [Download it](http://www.vagrantup.com/)
and then `cd vagrant` followed by `vagrant up` to create your working
development environment. Once your environment has been created, run
`vagrant ssh` and follow the next two instructions.

Create the Database Schema
--------------------------

In your terminal, type

    (batter) $ python batter/batter/manage.py syncdb
    (batter) $ python batter/batter/manage.py migrate

Run Batter
----------

In your terminal, type

    (batter) $ python batter/batter/manage.py runserver 0.0.0.0:8000

You should now be able to open your browser to http://localhost:8080/ and
use the site.

Yes, you're running the server on port 8000 in your vagrant environment,
but vagrant port-forwards environment:8000 to localhost:8080.

Contribute changes!
-------------------

So you want to contribute to Batter, you devilishly smart and attractive
person? Awesome!

First off, fork the [wafflesfm/batter](https://github.com/wafflesfm/batter)
repository to your own github account. After you've cloned your own fork,
add the wafflesfm repo as the `upstream` remote with

    $ git remote add upstream git@github.com:wafflesfm/batter

(If you have commit access to wafflesfm/batter, you don't need to fork
or add the upstream remote. The rest of this section still applies to you!)

### Styleguide

Please follow these **coding standards** when writing code:

* Poocoo [styleguide] [poocoo] for all Python code.
* For Django-specific code follow internal Django [coding style] [django].
* Additionally, since we want Batter to be Python3 compatible,
  make sure your code complies with Django [guidelines] [python3]
  on Python3 compatibility.

[poocoo]: http://pocoo.org/internal/styleguide/#styleguide
[django]: http://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style
[python3]: https://docs.djangoproject.com/en/dev/topics/python3

### i18n

We want Batter to be **translatable**, so please use Django's builtin
internationalization
[helpers](https://docs.djangoproject.com/en/dev/topics/i18n/translation)
for all strings displayed to the user.

### Workflow

We use [git-flow](https://github.com/nvie/gitflow) for our git workflow.
Debian/Ubuntu users can `sudo aptitude install git-flow`, and users of
other operating systems can find installation instructions
[here](https://github.com/nvie/gitflow/wiki/Installation).

Once you have git-flow installed, you need to set it up for your batter
repository. Setting up git-flow is a one-time thing. After you clone the repository
and installed git-flow, navigate to your batter project folder and run

    $ git flow init

Accept all the defaults. After the setup wizard is done, your "stable"
branch should be **master**, "development" branch should be **develop**,
"feature" prefix should be **feature**, "release" prefix should be
**release**, "hotfix" prefix should be **hotfix**, and "support" prefix
should be **support**.

After this, you can use git flow to work on new features or fix existing
ones. The following articles should help you understand how git-flow works.

* http://nvie.com/posts/a-successful-git-branching-model/ - the original
  blog post introducing the git workflow

* http://yakiloo.com/getting-started-git-flow/ - a practical introduction
  to using the git-flow plugin

* http://qq.is/article/git-flow-on-github - using git-flow in tandem with
  GitHub pull requests.

It is *strongly recommended* that
even committers who have access to the repository use GitHub pull requests
to merge their code. If you do this, then our
[code testing](https://travis-ci.org/wafflesfm/batter) and
[code coverage](https://coveralls.io/r/wafflesfm/batter) tools will
automatically tell you if what you are about to merge is going to break
everything, and will automatically remind you to write any necessary tests.
