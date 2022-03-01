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

from PyQt5.QtCore import QThread, pyqtSignal, QObject

class LHWorker(QThread):
    lh_path = "C:\\Users\\Master\\projects\\tundra_tools\\bin\\lighthouse\\win32\\lighthouse_console.exe"
    lh = None
    lh_console_open = False;
    console_close = pyqtSignal()
    console_open = pyqtSignal()
    devinfo_ready = pyqtSignal(list)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        return

    def __del__(self, parent=None):
        self.wait()
        return

    def run(self):
        self.lh = pexpect.popen_spawn.PopenSpawn(self.lh_path)
        lh_console_open = True
        i = self.lh.expect('lh>')
        opendata = self.lh.before
        self.console_open.emit()
        self.get_devinfo()


    def close_console(self):
        self.lh.sendline('quit\r\n')
        self.lh.wait()


    def identify_device(self, serial):
        self.lh.sendline('identifycontroller\r\n')
        self.lh.expect('lh>')


    def connect_device(self, serial):
        cmd = f"serial {serial}\r\n"
        self.lh.sendline(cmd)
        self.lh.expect('lh>')
        

    def get_devinfo(self):
        self.lh.sendline('deviceinfo\r\n')
        self.lh.expect('lh>')
        devinfo_data = self.lh.before.decode('utf-8')
        devinfo_parts = devinfo_data.split('\r\n')
        num_lines = len(devinfo_parts) - 1
        num_devices = num_lines/2
        print("Number of devices found: ", num_devices)
        result = []

        ct = 0;
        while ct < num_lines:
            tracker = Tracker()
            line1 = devinfo_parts[ct]
            ct = ct + 1
            line2 = devinfo_parts[ct]
            ct = ct + 1
            tracker.instantiate_from_raw(line1, line2)
            result.append(tracker)

        self.devinfo_ready.emit(result)
