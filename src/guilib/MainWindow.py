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
        print("Scan Button Pressed!")
