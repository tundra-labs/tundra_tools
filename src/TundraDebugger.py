#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import time
import subprocess
import signal
import pexpect
import re
import configparser

from pprint import pprint
from pexpect import popen_spawn
from pylib.Tracker import Tracker
from PyQt5.QtWidgets import QApplication

import guilib.MainWindow as gui

basedir = os.path.dirname(__file__)

# Set the process name as you want it to appear in Task Manager
try:
    from ctypes import windll
    myappid = 'com.TundraLabs.apps.TundraDebugger'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    # Read the base config, to get the actual config.  If the directories, don't exist, create and initialize
    config = None
    base_config = configparser.ConfigParser()

    # These defaults should be changed before release to utilize the current users Documents Directory
    base_config['DEFAULT'] = {
        'LighthouseConsolePath': 'lighthouse_console.exe',
        'StoragePath': "C:\\Users\\Master\\Documents\\TundraDebugger",
        'IniPath': "C:\\Users\\Master\\Documents\\TundraDebugger\\TundraDebugger.ini",
        'LHConfigs': "C:\\Users\\Master\\Documents\\TundraDebugger\\Configs"
    }

    if not os.path.isdir(base_config['DEFAULT']['StoragePath']):
        os.makedirs(base_config['DEFAULT']['LHConfigs'])
        with open(base_config['DEFAULT']['IniPath'], 'w') as configfile:
            base_config.write(configfile)

        config = base_config
    else:
        config = configparser.ConfigParser()
        config.read(base_config['DEFAULT']['IniPath'])

    #print("LighthouseConsolePath: ", config['DEFAULT']['LighthouseConsolePath'])
    #print("StoragePath: ", config['DEFAULT']['StoragePath'])
    #print("IniPath: ", config['DEFAULT']['IniPath'])
    #print("LHConfigs: ", config['DEFAULT']['LHConfigs'])

    # Start gui portion
    app = QApplication(sys.argv)
    window = gui.MainWindow(None, config)
    window.show()

    sys.exit(app.exec())
