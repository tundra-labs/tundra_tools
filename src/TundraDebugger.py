#!/usr/bin/env python

import sys
import os

from PyQt5.QtWidgets import QApplication

import guilib.MainWindow as gui

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = gui.MainWindow(None, "guilib\\stylesheets\\MainWindow.stylesheet")
    window.show()

    sys.exit(app.exec())
