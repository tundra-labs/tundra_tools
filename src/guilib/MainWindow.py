import sys
import time
import subprocess
import signal
import pexpect
import re

from pylib.Tracker import Tracker
from guilib.LHWorker import LHWorker
from pexpect import popen_spawn

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QMenuBar,
    QMenu, QAction, QVBoxLayout, QHBoxLayout, QStackedLayout,
    QWidget, QTableWidget
)

lighthouse_connected = False


class MainWindow(QMainWindow):
    style_path = "guilib\\stylesheets\\MainWindow.stylesheet"

    def __init__(self, parent=None):
        super().__init__()
        self.startUI()

    def startUI(self):
        self.lhworker = LHWorker()
        self.lhworker.console_open.connect(self.update_connect_ui_on)
        self.lhworker.console_close.connect(self.update_connect_ui_off)
        self.lhworker.devinfo_ready.connect(self.update_devtable_ui)

        if self.style_path != None:
            with open(self.style_path, "r") as spfh:
                self.setStyleSheet(spfh.read())

        self.setObjectName("MainWindow")
        self.setWindowTitle("Tundra Debugger")
        self.resize(1280, 960)
        self.create_menu_bar()

        page_layout = QVBoxLayout()
        status_label_layout = QHBoxLayout()
        top_label_layout = QHBoxLayout()
        top_button_layout = QHBoxLayout()
        middle_table_layout = QHBoxLayout()
        stack_layout = QStackedLayout()

        page_layout.addLayout(top_label_layout)
        page_layout.addLayout(top_button_layout)
        page_layout.addLayout(status_label_layout)
        page_layout.addLayout(middle_table_layout)
        page_layout.addLayout(stack_layout)

        self.status_label = QLabel("Not Connected")
        self.status_label.setObjectName("StatusLabel")
        status_label_layout.addWidget(self.status_label)
        status_label_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        top_label = QLabel("Tundra Tracker Debugging Tool")
        top_label.setObjectName("TitleLabel")
        top_label_layout.addWidget(top_label)
        top_label_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.button = QPushButton("Scan For Devices")
        self.button.setCheckable(True)
        self.button.setFixedWidth(240)
        self.button.setFixedHeight(30)
        self.button.clicked.connect(self.scan_button_pressed)
        top_button_layout.addWidget(self.button)

        self.tableWidget = QTableWidget()
        self.tableWidget.setObjectName("DeviceTable")
        self.tableWidget.setColumnCount(6)
        header_labels = ['Device', 'Class', 'Vid/Pid', 'Config Data', '', '']
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        middle_table_layout.addWidget(self.tableWidget)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)


    def update_devtable_ui(self, devices):
        numdevs = len(devices)
        self.tableWidget.setRowCount(numdevs)


    def update_connect_ui_on(self):
        self.status_label.setText("Connected.")


    def update_connect_ui_off(self):
        self.status_label.setText("Not Connected.")


    def create_menu_bar(self):
        menu_bar = self.menuBar()
        newAct = QAction('&Exit', self)
        openAct = QAction('&Open', self)
        saveAct = QAction('&Save', self)
        exitAct = QAction('&Exit', self)
        exitAct.triggered.connect(self.exitAction)

        copyAct = QAction('&Copy', self)
        pasteAct = QAction('&Paste', self)
        helpContentAct = QAction('&Help', self)
        aboutAct = QAction('&About', self)

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(newAct)
        file_menu.addAction(openAct)
        file_menu.addAction(saveAct)
        file_menu.addAction(exitAct)

        edit_menu = menu_bar.addMenu('&Edit')
        edit_menu.addAction(copyAct)
        edit_menu.addAction(pasteAct)

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(helpContentAct)
        help_menu.addSeparator()
        help_menu.addAction(aboutAct)

    def newAction(self):
        print("New Action selected")

    def openAction(self):
        print("Open Action selected")

    def saveAction(self):
        print("Save Action selected")

    def exitAction(self):
        print("Exit Action selected")
        sys.exit(0)

    def copyAction(self):
        print("Copy Action selected")

    def pasteAction(self):
        print("Paste Action selected")

    def helpContentAction(self):
        print("Help Content Action selected")

    def aboutAction(self):
        print("New Action selected")


    def scan_button_pressed(self):
        self.lhworker.start()
        #self.lhworker.get_devinfo()
