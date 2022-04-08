import sys
import time
import subprocess
import signal
import pexpect
import re
from os.path import exists

from functools import partial

from pylib.Tracker import Tracker
from guilib.LHWorker import LHWorker
from pexpect import popen_spawn

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QMenuBar,
    QMenu, QAction, QVBoxLayout, QHBoxLayout, QStackedLayout,
    QWidget, QTableWidget, QTableWidgetItem, QFrame
)

from guilib.TrackerWindowStyle import tracker_window_style

class TrackerWindow(QMainWindow):
    serial = ""
    lhworker = None

    def __init__(self, parent=None, serial="", worker=None, appconfig=None):
        super().__init__()
        self.serial = serial
        self.lhworker = worker
        self.device = self.lhworker.get_device_by_serial(serial)
        self.appConfig = appconfig
        self.startUI()

    def load_stylesheet(self):
        self.setStyleSheet(tracker_window_style)

    def startUI(self):
        #if self.style_path != None:
        #    with open(self.style_path, "r") as spfh:
        #        self.setStyleSheet(spfh.read())

        self.load_stylesheet()
        title = f"Tundra Debugger :: Device Window :: {self.serial}"
        self.setObjectName("TrackerWindow")
        self.setWindowTitle(title)
        self.resize(1280, 960)

        page_layout = QVBoxLayout()

        devinfo_layout = QHBoxLayout()

        section1_layout = QHBoxLayout()
        action_button_layout = QHBoxLayout()

        stack_layout = QStackedLayout()

        page_layout.addLayout(devinfo_layout)
        page_layout.addLayout(section1_layout)
        page_layout.addLayout(stack_layout)

        section1_layout.addLayout(action_button_layout)

        self.build_devinfo_layout(devinfo_layout)
        self.build_action_layout(action_button_layout)


        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)


    def build_devinfo_layout(self, layout):
        label = QLabel("Serial: " + self.serial)
        layout.addWidget(label)
        #layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        label2 = QLabel("Vid/Pid: " + self.device.vid + " / " + self.device.pid)
        layout.addWidget(label2)
        label3 = QLabel("Device Class: " + self.device.devclass)
        layout.addWidget(label3)


    def build_action_layout(self, layout):
        self.imu_button = QPushButton("Get IMU Sample")
        self.imu_button.setCheckable(True)
        self.imu_button.clicked.connect(self.imu_button_pressed)
        layout.addWidget(self.imu_button)

        self.sensor_button = QPushButton("Download Json Configuration")
        self.sensor_button.setCheckable(True)
        self.sensor_button.clicked.connect(self.download_button_pressed)
        layout.addWidget(self.sensor_button)

        self.download_button = QPushButton("Upload Json Configuration")
        self.download_button.setCheckable(True)
        self.download_button.clicked.connect(self.upload_button_pressed)
        layout.addWidget(self.download_button)

        self.upload_button = QPushButton("Get Optical Sensor Sample")
        self.upload_button.setCheckable(True)
        self.upload_button.clicked.connect(self.sensor_button_pressed)
        layout.addWidget(self.upload_button)



    def imu_button_pressed(self):
        return


    def sensor_button_pressed(self):
        return


    def download_button_pressed(self):
        self.lhworker.get_json_config(self.serial)
        return


    def upload_button_pressed(self):
        return
