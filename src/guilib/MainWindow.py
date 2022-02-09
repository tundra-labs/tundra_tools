import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMenuBar, QMenu, QAction
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None, style_path=None):
        super().__init__()

        if style_path != None:
            with open(style_path, "r") as spfh:
                self.setStyleSheet(spfh.read())

        #self.setStyleSheet("background-color: black;")
        self.setObjectName("MainWindow")
        self.setWindowTitle("Tundra Debugger")
        self.resize(1280, 960)
        self.create_menu_bar()

        #self.centralWidget = QLabel("Tundra Tracker Debugging Tool")
        #self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        #self.setCentralWidget(self.centralWidget)

        button = QPushButton("Scan For Devices")
        button.setCheckable(True)
        button.setFixedWidth(120)
        button.setFixedHeight(26)
        button.clicked.connect(self.scan_button_pressed)
        self.setCentralWidget(button)


    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        menu_bar.setObjectName("appMenuBar")
        self.setMenuBar(menu_bar)
        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)

        self.newAction = QAction(self)
        self.openAction = QAction(self)
        self.saveAction = QAction(self)
        self.exitAction = QAction(self)
        self.copyAction = QAction(self)
        self.pasteAction = QAction(self)
        self.cutAction = QAction(self)
        self.helpContentAction = QAction(self)
        self.aboutAction = QAction(self)

        menu_bar.addMenu(file_menu)
        file_menu.addAction(self.newAction)
        file_menu.addAction(self.openAction)
        file_menu.addAction(self.saveAction)
        file_menu.addSeparator()
        file_menu.addAction(self.exitAction)

        menu_bar.addMenu(edit_menu)
        edit_menu.addAction(self.copyAction)
        edit_menu.addAction(self.pasteAction)
        edit_menu.addAction(self.cutAction)

        menu_bar.addMenu(help_menu)
        help_menu.addAction(self.helpContentAction)
        help_menu.addSeparator()
        help_menu.addAction(self.aboutAction)


    def newAction(self, method):
        print("New Action selected")

    def openAction(self, method):
        print("Open Action selected")

    def saveAction(self, method):
        print("Save Action selected")

    def exitAction(self, method):
        print("Exit Action selected")
        sys.exit(0)

    def copyAction(self, method):
        print("Copy Action selected")

    def pasteAction(self, method):
        print("Paste Action selected")

    def cutAction(self, method):
        print("Cut Action selected")

    def helpContentAction(self, method):
        print("Help Content Action selected")

    def aboutAction(self, method):
        print("New Action selected")


    def scan_button_pressed(self):
        print("Scan Button Pressed!")
