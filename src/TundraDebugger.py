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

from pexpect import popen_spawn
from pylib.Tracker import Tracker

from PyQt5.QtWidgets import QApplication

import guilib.MainWindow as gui

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll
    myappid = 'com.TundraLabs.apps.TundraDebugger'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = gui.MainWindow(None)
    window.show()

    sys.exit(app.exec())
