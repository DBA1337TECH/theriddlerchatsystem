"""
DBA 1337_TECH, AUSTIN TEXAS © July 2021
Proof of Concept code, No liabilities or warranties expressed or implied.
"""
"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
import math

from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import QWidget


class Overlay(QWidget):
    def __init__(self, parent: QWidget = None):
        super(Overlay, self).__init__(parent)
        self.setPalette(Qt.transparent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(parent.width() + 75 , parent.height()/2 - 25, 100, 100)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 140, 140, 0)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5) * 32, 153, 300)))
            else:
                painter.setBrush(QBrush(QColor(240, 40, 40)))
            painter.drawEllipse(
                self.frameGeometry().width() / 2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.frameGeometry().height() / 2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20

            )
        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(50)
        self.counter = 0

    def resizeEvent(self, event):
        self.resize(event.size())
        event.accept()

    def timerEvent(self, event):
        self.counter += 1
        self.update()

        if self.counter == 60:
            self.killTimer(self.timer)
            self.hide()
