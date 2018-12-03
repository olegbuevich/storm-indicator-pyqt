# storm-indicator-pyqt

PyQt based indicator for connecting to your SSH hosts easily.

**storm-indicator-pyqt** uses [~/.ssh/config](http://linux.die.net/man/5/ssh_config) files to list SSH connections. If you don't use your SSH config file yet,  you can optionally use [storm](http://www.github.com/emre/storm)
to easily add your servers.
Based on [emre/storm-indicator](https://github.com/emre/storm-indicator)

## requirements

* envparse
* PyQt5
* stormssh

## installation

```bash
python setup.py install
```

## running

```bash
ssh-indicator-pyqt
# or
SHELLEM="gnome-terminal --" ssh-indicator-pyqt
```
