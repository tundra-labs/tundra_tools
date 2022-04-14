#!/usr/bin/env python

# ---
# Tracker class, will instantiate an object and set it's parameters based on the 2 lines of read_output
# from lighthouse_console.exe::deviceinfo
#
# Parsing will have to be updated should the output from the deviceinfo command change.
# ---

class Tracker:
    def __init__(self):
        self.serial = ""
        self.devclass = ""
        self.config_compressed = 0
        self.config_inflated = 0
        self.vid = 0
        self.pid = 0
        self.watchman_board_model = ""
        self.watchman_version = ""
        self.hardware_revision = ""
        self.vrc_version = ""
        self.radio_version = ""


    def __str__(self):
        result = (f"Tracker device {self.serial}:\n" +
                  f"   device class: {self.devclass}\n" +
                  f"   vid: {self.vid}\n" +
                  f"   pid: {self.pid}\n" +
                  f"   config data: {self.config_compressed} bytes compressed, expands to {self.config_inflated} bytes.\n" +
                  f"   Watchman Board Model: {self.watchman_board_model}\n" +
                  f"   Watchman Version: {self.watchman_version}\n" +
                  f"   Hardware Revision: {self.hardware_revision}\n" +
                  f"   VRC Version: {self.vrc_version}\n" +
                  f"   Radio Version: {self.radio_version}\n")
        return result

    def instantiate_from_raw(self, line1="", line2=""):
        l1_parts = line1.split()
        l2_parts = line2.split()
        t0 = l2_parts[1].split("=")
        t0_serial = t0[1]

        l1_serial = l1_parts[0].strip(":")
        if l1_serial != t0_serial:
            print(f"Error, mismatched device lines from lh_console. {l1_parts[0]} != {t0_serial}")
            return False

        self.serial = l1_serial
        self.config_compressed = l1_parts[4]
        self.config_inflated = l1_parts[13]
        self.vid = l1_parts[7][5:].strip(",")
        self.pid = l1_parts[8][4:].strip("]")

        t1 = l2_parts[2].split("=")
        self.devclass = t1[1]

        return True
