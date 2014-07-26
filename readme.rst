
======================================
 Entchen --- irc bot based on Twisted
======================================

Install
=======

* Set up virtualenv: `mkvirtualenv --no-site-packages entchen`
* On debian or ubuntu install `libffi-dev`; on other distributions find and install its equivalent
* Install requirements from requirements.d/base.txt: `pip install -r requirements.d/base.txt`
* Modify main.py for your needs


Todos
=====

 * Lots of cleanup
 * Documentation
 * .help for commands / plugins
 * Some kind of acl for sensitive commands (i.e. git, sysinfo, ...)
 * Plugin for adding rtm tasks to a user (via api or via email)
