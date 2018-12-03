import os
from subprocess import Popen
import sys

from envparse import env
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QMessageBox, QSystemTrayIcon


class StormIndicator(QMainWindow):
    def __init__(self):
        super(StormIndicator, self).__init__()
        self.tray_icon = QSystemTrayIcon(
            QIcon(os.path.dirname(os.path.realpath(__file__)) + '/icons/tray.svg'),
            self)
        self.tray_icon_menu = QMenu(self)
        self.resize(0, 0)
        self.shell_emulator = self._get_shell_emulator()

    @staticmethod
    def _get_shell_emulator():
        """
        rtype: list
        """
        config_file = os.path.expanduser('~') + '/.storm-indicator'
        if os.path.isfile(config_file):
            env.read_envfile(config_file)
        return env.str('SHELLEM', default='gnome-terminal --').split(' ')

    def setup_menu(self):
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def menu_item_callback(self):
        sender = self.sender()
        if isinstance(sender, QAction):
            identifier = sender.data()
            if not isinstance(identifier, str):
                sys.exit(1)
            if identifier == 'about':
                self.pop_dialog(
                    '<b>storm-indicator-pyqt</b> is a helper for connecting to your servers easily.<br>'
                    'Based on <a href="https://github.com/emre/storm-indicator">emre/storm-indicator</a><br>'
                    'You can use the <a href="https://github.com/olegbuevich/storm-indicator/issues">issue '
                    'tracker</a> for bug reports and feature requests')
            elif identifier == 'quit':
                sys.exit(0)
            else:
                command = self.shell_emulator + [
                    '/bin/bash',
                    '-c',
                    'ssh {host}; bash;'.format(host=identifier)
                ]
                self.run_program(command)

    def add_hosts_menu_items(self, items: dict = None):
        if not isinstance(items, dict):
            return
        for item in sorted(items.keys()):
            if not items.get(item):
                menu_item = self.tray_icon_menu.addAction(item)
                menu_item.setData(item)
                menu_item.triggered.connect(self.menu_item_callback)
            else:
                submenu = QMenu(item, self.tray_icon_menu)
                for host in items.get(item):
                    host_item = submenu.addAction(host)
                    host_item.setData(host)
                    host_item.triggered.connect(self.menu_item_callback)
                    if host == item:
                        submenu.addSeparator()
                self.tray_icon_menu.addMenu(submenu)

    def add_menu_item(self, text: str, value: str = None, sensitive: bool = True):
        if not isinstance(text, str) or not isinstance(sensitive, bool):
            return

        menu_item = self.tray_icon_menu.addAction(text)
        menu_item.setEnabled(sensitive)
        menu_item.setData(value)
        if sensitive:
            menu_item.triggered.connect(self.menu_item_callback)

    def add_separator(self):
        self.tray_icon_menu.addSeparator()

    @staticmethod
    def run_program(cmd):
        Popen(cmd)

    @staticmethod
    def pop_dialog(message: str = None):
        if not message:
            return
        QMessageBox.information(None, 'storm-indicator', message, QMessageBox.Ok)
