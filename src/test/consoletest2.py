#!/usr/bin/env python


from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time
import subprocess
import signal
import pexpect
import re

from pylib.Tracker import Tracker

from pexpect import popen_spawn

def get_devinfo(phandle=None):
    if phandle is None:
        return None

    phandle.sendline('deviceinfo\r\n')
    phandle.expect('lh>')
    devinfo_data = phandle.before.decode('utf-8')
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

    return result

def main():

    lh = pexpect.popen_spawn.PopenSpawn("..\\bin\\lighthouse\\win32\\lighthouse_console.exe")
    #fout = file("LOG.TXT", "wb")
    #lh.logfile_read = fout

    i = lh.expect('lh>')
    opendata = lh.before

    device_data = get_devinfo(lh)

    for device in device_data:
        print(device)

    print("Exit")
    lh.kill(signal.SIGTERM)


if __name__ == '__main__':
    main()
    sys.exit(0)
