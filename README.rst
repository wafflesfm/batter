========================
Batter
========================

It makes Waffles.

To develop on this project follow these steps:

#. Download the code
#. Create your working environment
#. Install dependencies
#. Create the database schema
#. Run Batter
#. Contribute changes!

Download the code
=================

You can get the most recent copy of Batter by cloning this repository:

    git clone git://github.com/wafflesfm/batter.git

which will copy all of Batter into a new folder called `batter`.

Create your Working Environment
===============================

First, make sure you have downloaded virtualenv (http://www.virtualenv.org).
Once that's installed, create a new virtualenv inside of the `batter`
folder:

    $ cd batter

    $ virtualenv --distribute venv

    $ source venv/bin/activate

Your terminal prompt should now look like this:

    (venv) $ 

Install Dependencies
====================

In your terminal, type

    (venv) $ pip install -r requirements/local.txt

You should see a list of packages being downloaded and installed.

Create the Database Schema
============================

In your terminal, type

    (venv) $ python batter/manage.py syncdb

    (venv) $ python batter/manage.py migrate

Run Batter
==========

In your terminal, type

    (venv) $ python batter/manage.py runserver

You should now be able to open your browser to http://localhost:800/ and
use the site.

Contribute changes!
===================

So you want to contribute to Batter, you devilishly smart and attractive
person? Awesome!

First off, fork the wafflesfm/batter (https://github.com/wafflesfm/batter)
repository to your own github account. After you've cloned your own fork,
add the wafflesfm repo as the `upstream` remote with

    $ git remote add upstream git@github.com:wafflesfm/batter

(If you have commit access to wafflesfm/batter, you don't need to fork
or add the upstream remote. The rest of this section still applies to you!)

We use git-flow (https://github.com/nvie/gitflow) for our git workflow.
Debian/Ubuntu users can `sudo aptitude install git-flow`, and users of
other operating systems can find installation instructions here:
https://github.com/nvie/gitflow/wiki/Installation

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
