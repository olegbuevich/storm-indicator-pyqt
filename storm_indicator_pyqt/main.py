import logging
import sys

from PyQt5.QtCore import qInstallMessageHandler, QtCriticalMsg, QtFatalMsg, QtInfoMsg, QtWarningMsg
from PyQt5.QtWidgets import QApplication
try:
    import storm
except ImportError:
    raise ImportError(
        'stormssh is not installed.\n'
        'You need to install it in order to use storm-indicator.\n'
        'Try "pip install stormssh".')

from storm_indicator_pyqt.storm_ind import StormIndicator


# init logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
LOG = logging.getLogger('ssh-indicator-pyqt')


def qt_message_handler(mode, context, message):
    """Redirect Qt log messages to python logging."""
    if mode == QtInfoMsg:
        LOG.info(message)
    elif mode == QtWarningMsg:
        LOG.warning(message)
    elif mode == QtCriticalMsg:
        LOG.critical(message)
    elif mode == QtFatalMsg:
        LOG.critical(message)
    else:
        LOG.debug(message)
    LOG.debug('qt_message_handler: line: %d, func: %s(), file: %s',
              context.line, context.function, context.file)


def main(argv):
    """Parse ssh .config file and run application."""
    LOG.debug('args: %s', argv)
    qInstallMessageHandler(qt_message_handler)

    app = QApplication([])

    indicator = StormIndicator()
    indicator.add_menu_item('SSH Connections', sensitive=False)
    indicator.add_separator()

    hosts = {}

    # loop for all entries except blank line and wildcard entries
    for host in [host.get('host') for host in storm.ConfigParser().load()
                 if host.get('host') and '*' not in host.get('host')]:
        assert isinstance(host, str)
        # '-' is a delimiter
        # Example: Host1 - parent host, Host1-dev1 - child host
        if '-' in host:
            parent = host.split('-')[0]
            if parent in hosts.keys():
                if hosts.get(parent):
                    hosts[parent].append(host)
                else:
                    hosts[parent] = []
                    hosts[parent].append(parent)
                    hosts[parent].append(host)
            else:
                is_new_item = True
                for key in hosts:
                    if parent in key:
                        is_new_item = False
                        hosts[parent] = []
                        hosts[parent].append(key)
                        hosts[parent].append(host)
                        del hosts[key]
                        break
                if is_new_item:
                    hosts[host] = None
        else:
            hosts[host] = None
    indicator.add_hosts_menu_items(hosts)

    indicator.add_separator()
    indicator.add_menu_item('About', value='about')
    indicator.add_separator()
    indicator.add_menu_item('Quit', value='quit')
    indicator.show()
    indicator.setup_menu()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
