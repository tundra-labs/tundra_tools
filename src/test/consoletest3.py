#!/usr/bin/env python

# gotten from https://wiki.python.org/moin/PyQt5/Threading%2C_Signals_and_Slots, for study purposes

import math, random, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.thread = Worker()
        label = QLabel(self.tr("Number of stars:"))

        self.spinBox = QSpinBox()
        self.spinBox.setMaximum(10000)
        self.spinBox.setValue(100)
        self.startButton = QPushButton(self.tr("&Start"))
        self.viewer = QLabel()
        self.viewer.setFixedSize(300, 300)

        self.thread.finished.connect(self.updateUi)
        #self.thread.terminated.connect(self.updateUi)
        self.thread.output['QRect', 'QImage'].connect(self.addImage)
        self.startButton.clicked.connect(self.makePicture)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.spinBox, 0, 1)
        layout.addWidget(self.startButton, 0, 2)
        layout.addWidget(self.viewer, 1, 0, 1, 3)
        self.setLayout(layout)
        self.setWindowTitle(self.tr("Simple Threading Example"))

    def makePicture(self):
        self.spinBox.setReadOnly(True)
        self.startButton.setEnabled(False)
        pixmap = QPixmap(self.viewer.size())
        pixmap.fill(Qt.black)
        self.viewer.setPixmap(pixmap)
        self.thread.render(self.viewer.size(), self.spinBox.value())

    def addImage(self, rect, image):
        pixmap = self.viewer.pixmap()
        painter = QPainter()
        painter.begin(pixmap)
        painter.drawImage(rect, image)
        painter.end()
        self.viewer.update(rect)

    def updateUi(self):
        self.spinBox.setReadOnly(False)
        self.startButton.setEnabled(True)


class Worker(QThread):
    output = pyqtSignal(QRect, QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.size = QSize(0, 0)
        self.stars = 0

        self.path = QPainterPath()
        angle = 2*math.pi/5
        self.outerRadius = 20
        self.innerRadius = 8
        self.path.moveTo(self.outerRadius, 0)
        for step in range(1, 6):
            self.path.lineTo(
                self.innerRadius * math.cos((step - 0.5) * angle),
                self.innerRadius * math.sin((step - 0.5) * angle)
            )

        self.path.closeSubpath()

    def __del__(self):
        self.exiting = True
        self.wait()

    def render(self, size, stars):
        self.size = size
        self.stars = stars
        self.start()

    def run(self):
        # Note: this is never called directly, called by Qt on thread env setup
        random.seed()
        n = self.stars
        width = self.size.width()
        height = self.size.height()

        while not self.exiting and n > 0:
            image = QImage(self.outerRadius * 2, self.outerRadius * 2, QImage.Format_ARGB32)
            image.fill(qRgba(0, 0, 0, 0))
            x = random.randrange(0, width)
            y = random.randrange(0, height)
            angle = random.randrange(0, 360)
            red = random.randrange(0, 256)
            green = random.randrange(0, 256)
            blue = random.randrange(0, 256)
            alpha = random.randrange(0, 256)

            painter = QPainter()
            painter.begin(image)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(red, green, blue, alpha))
            painter.translate(self.outerRadius, self.outerRadius)
            painter.rotate(angle)
            painter.drawPath(self.path)
            painter.end()

            self.output.emit(QRect(x - self.outerRadius, y - self.outerRadius, self.outerRadius * 2, self.outerRadius * 2), image)
            n -= 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
