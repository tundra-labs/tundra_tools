from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time
import subprocess
import signal
import pexpect
import re

from datetime import datetime
from pexpect import popen_spawn
from pylib.Tracker import Tracker
from PyQt5.QtCore import QThread, pyqtSignal, QObject

class LHWorker(QThread):
    lh_path = ""
    appConfig = None
    lh = None
    lh_console_open = False;
    console_close = pyqtSignal()
    console_open = pyqtSignal()
    devinfo_ready = pyqtSignal(list)
    devices = []

    def __init__(self, parent=None, appconfig=None):
        QThread.__init__(self, parent)
        if appconfig == None:
            self.lh_path = "lighthouse_console.exe"
        else:
            self.appConfig = appconfig
            self.lh_path = self.appConfig['DEFAULT']['LighthouseConsolePath']
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
        self.lh.sendline('quit')
        self.lh.wait()

    def identify_device(self, serial):
        self.lh.sendline('identifycontroller')
        self.lh.expect('lh>')

    def connect_device(self, serial):
        cmd = f"serial {serial}"
        self.lh.sendline(cmd)
        self.lh.expect('lh>')
        self.get_hw_version(serial)

    def get_device_by_serial(self, serial):
        for tracker in self.devices:
            if tracker.serial == serial:
                return tracker

    # XXX:
    # Currently, the output of this command from lighthouse_console is not consistent, the VRC Version doesn't include a ':' character
    # Keep this in mind should lighthouse_console ever update
    def get_hw_version(self, serial):
        tracker = self.get_device_by_serial(serial)
        self.lh.sendline('version')
        self.lh.expect('lh>')
        vdata = self.lh.before
        version_data = vdata.decode('utf-8')
        version_parts = version_data.split('\r\n')
        for ol in version_parts:
            if(ol.startswith("VRC")):
                vrc_parts = ol.split(' ')
                tracker.vrc_version = vrc_parts[2]
            else:
                ol_parts = ol.split(':')
                sp0 = ol_parts[0].lstrip()
                if sp0 == "Watchman Board Model":
                    tracker.watchman_board_model = ol_parts[1]
                elif sp0 == "Watchman Version":
                    tracker.watchman_version = ol_parts[1]
                elif sp0 == "Hardware Revision":
                    tracker.hardware_revision = ol_parts[1]
                elif sp0 == "Radio Version":
                    tracker.radio_version = ol_parts[1]

    def get_devinfo(self):
        self.lh.sendline('deviceinfo')
        self.lh.expect('lh>')
        ddata = self.lh.before
        devinfo_data = ddata.decode('utf-8')
        devinfo_parts = devinfo_data.split('\r\n')
        num_lines = len(devinfo_parts) - 1
        num_devices = num_lines/2
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
            self.devices.append(tracker)

        self.devinfo_ready.emit(result)

    def get_json_config(self, serial):
        cur_datetime = datetime.now()
        datestr = cur_datetime.strftime("%Y%m%d%H%M%S")
        cfgdir = self.appConfig['DEFAULT']['LHConfigs']
        filename = cfgdir + "\\" + serial + "_" + datestr + ".json"
        cmd = f"downloadconfig {filename}"
        self.lh.sendline(cmd)
        self.lh.expect('lh>')

    def upload_json_config(self, serial, filePath):
        cmd = f"uploadconfig {filePath}"
        self.lh.sendline(cmd)
        self.lh.expect('lh>')
