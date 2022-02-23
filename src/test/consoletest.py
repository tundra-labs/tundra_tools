#!/usr/bin/env python

import pylib.LHconsole as lhc
import sys
import time
import subprocess
import signal


def main():

    my_console = lhc.LHconsole()

    def int_handler(sig, frame):
        print("exiting consoletest")
        my_console.lh_exit()
        sys.exit(0)


    signal.signal(signal.SIGINT, int_handler)

    my_console.start_background_thread()
    crud = my_console.read_cmd_output()

    #my_console.cmd("deviceinfo")
    #print(my_console.read_cmd_output())

    #my_console.lh_cleanup()
    sys.exit(0)
    #initial_crunk = my_console.read_output()
    #my_console.cmd("deviceinfo")
    #devinfo = my_console.read_output()
    #print(devinfo)

if __name__ == '__main__':
    main()
