import sys
import time
import subprocess
import signal
import pexpect
import re

from functools import partial
from os.path import exists

from pylib.Tracker import Tracker
from guilib.LHWorker import LHWorker
from guilib.TrackerWindow import TrackerWindow
from pexpect import popen_spawn

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QMenuBar,
    QMenu, QAction, QVBoxLayout, QHBoxLayout, QStackedLayout,
    QWidget, QTableWidget, QTableWidgetItem, QFrame
)

from guilib.MainWindowStyle import main_window_style

lighthouse_connected = False

class MainWindow(QMainWindow):
    def __init__(self, parent=None, appconfig=None):
        super().__init__()
        self.appConfig = appconfig
        self.startUI()

    def load_stylesheet(self):
        self.setStyleSheet(main_window_style)

    def startUI(self):
        self.lhworker = LHWorker(None, self.appConfig)
        self.lhworker.console_open.connect(self.update_connect_ui_on)
        self.lhworker.console_close.connect(self.update_connect_ui_off)
        self.lhworker.devinfo_ready.connect(self.update_devtable_ui)

        #if self.style_path != None:
            #with open(self.style_path, "r") as spfh:
                #self.setStyleSheet(spfh.read())

        self.load_stylesheet()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Tundra Debugger")
        self.resize(800, 800)
        self.create_menu_bar()

        self.identify_buttons = []
        self.select_buttons = []
        self.connected_serial = None

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
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 220)
        self.tableWidget.setColumnWidth(2, 230)
        #header_labels = ['Device', 'Class', 'Vid/Pid', 'Config Data', '', '']
        #header = self.tableWidget.horizontalHeader()
        #header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setFrameStyle(QFrame.Box | QFrame.Plain)
        #self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setFixedWidth(1000)
        self.tableWidget.setFixedHeight(450)
        middle_table_layout.addWidget(self.tableWidget, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)


    def format_table_cell(self, content):
        result = QTableWidgetItem(content)
        result.setTextAlignment(Qt.AlignHCenter)
        return result


    def update_devtable_ui(self, devices):
        self.devices = devices
        numdevs = len(devices)

        self.tableWidget.setRowCount(numdevs)
        self.identify_buttons = []
        self.select_buttons = []
        rowct = 0
        for device in devices:
            cell0 = self.format_table_cell(device.serial)
            self.tableWidget.setItem(rowct, 0, cell0)
            cell1 = self.format_table_cell(device.devclass)
            self.tableWidget.setItem(rowct, 1, cell1)
            vidpid = f"vid: {device.vid}  pid: {device.pid}"
            cell2 = self.format_table_cell(vidpid)
            self.tableWidget.setItem(rowct, 2, cell2)
            #cdata = f"Config: {device.config_inflated} bytes\n        {device.config_compressed} bytes compressed"
            #cell3 = self.format_table_cell(cdata)
            #self.tableWidget.setItem(rowct, 3, cell3)

            #idbutton = QPushButton("Identify")
            #idbutton.setObjectName(device.serial)
            #idbutton.setCheckable(True)
            #idbutton.clicked.connect(partial(self.id_button_pressed, device.serial))
            #self.identify_buttons.append(idbutton)
            #self.tableWidget.setCellWidget(rowct, 4, idbutton)

            conbutton = QPushButton("Connect")
            conbutton.setObjectName(device.serial)
            conbutton.setCheckable(True)
            conbutton.clicked.connect(partial(self.connect_button_pressed, device.serial))
            self.identify_buttons.append(conbutton)
            self.tableWidget.setCellWidget(rowct, 3, conbutton)

            rowct = rowct + 1

        #self.tableWidget.resizeToContents()


    def update_connect_ui_on(self):
        self.status_label.setText("Connected.")


    def update_connect_ui_off(self):
        self.status_label.setText("Not Connected.")


    def create_menu_bar(self):
        menu_bar = self.menuBar()
        newAct = QAction('&New', self)
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
        self.lhworker.close_console()
        sys.exit(0)

    def copyAction(self):
        print("Copy Action selected")

    def pasteAction(self):
        print("Paste Action selected")

    def helpContentAction(self):
        print("Help Content Action selected")

    def aboutAction(self):
        print("New Action selected")

    def id_button_pressed(self, serial):
        self.lhworker.identify_device(serial)

    def connect_button_pressed(self, serial):
        sending_button = self.sender()
        self.lhworker.connect_device(serial)
        self.connected_serial = serial
        self.device_window = TrackerWindow(self, serial, self.lhworker, self.appConfig)
        self.device_window.show()
        sending_button.setDefault(True)
        self.device_window.serial = serial;

    def scan_button_pressed(self):
        self.lhworker.start()
        #self.lhworker.get_devinfo()
