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

# This function will loop thru a config opbject and replace HOMEDIR with the actual contents of %USERPROFILE%
def convert_ini(config):
    configobj = config
    for key in configobj['DEFAULT']:
        if "HOMEDIR" in configobj['DEFAULT'][key]:
            tvalue = configobj['DEFAULT'][key].replace("HOMEDIR", homedir)
            configobj['DEFAULT'][key] = tvalue
    return configobj


if __name__ == "__main__":
    # Read the base config, to get the actual config.  If the directories, don't exist, create and initialize
    config = None
    bconfig = configparser.ConfigParser()

    # These defaults should be changed before release to utilize the current users Documents Directory
    bconfig['DEFAULT'] = {
        'LighthouseConsolePath': 'lighthouse_console.exe',
        'StoragePath': r"HOMEDIR\Documents\TundraDebugger",
        'IniPath': r"HOMEDIR\Documents\TundraDebugger\TundraDebugger.ini",
        'LHConfigs': r"HOMEDIR\Documents\TundraDebugger\Configs"
    }

    # Loop thru and replace all instances of HOMEDIR with the results of %USERPROFILE%
    homedir = os.getenv("USERPROFILE")
    base_config = convert_ini(bconfig)

    if not os.path.isdir(base_config['DEFAULT']['StoragePath']):
        os.makedirs(base_config['DEFAULT']['LHConfigs'])
        with open(base_config['DEFAULT']['IniPath'], 'w') as configfile:
            base_config.write(configfile)

        config = base_config
    else:
        cfg = configparser.ConfigParser()
        cfg.read(base_config['DEFAULT']['IniPath'])
        config = convert_ini(cfg)

    #print("LighthouseConsolePath: ", config['DEFAULT']['LighthouseConsolePath'])
    #print("StoragePath: ", config['DEFAULT']['StoragePath'])
    #print("IniPath: ", config['DEFAULT']['IniPath'])
    #print("LHConfigs: ", config['DEFAULT']['LHConfigs'])

    # Start gui portion
    app = QApplication(sys.argv)
    window = gui.MainWindow(None, config)
    window.show()

    sys.exit(app.exec())
