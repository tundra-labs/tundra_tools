from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time
import subprocess
import signal
import pexpect
import re

from pexpect import popen_spawn

from pylib.Tracker import Tracker

from PyQt5.QtCore import QThread, pyqtSignal

class LHWorker(QThread):
    console_close = pyqtSignal()
    console_open = pyqtSignal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        return

    def __del__(self, parent=None):
        return

    def run(self):
        return
