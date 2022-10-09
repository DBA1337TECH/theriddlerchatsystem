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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class SecretTextBox(QLineEdit):
    clicked = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        super(SecretTextBox, self).__init__(parent, **kwargs)
        s = self.size()
        print(self.size())
        print(parent.size())
        print(self.geometry())
        self.setGeometry(parent.width() / 2 - s.width() / 2,
                         parent.height() / 2 - s.height() / 2,
                         s.width(),
                         s.height()
                         )

    def mousePressEvent(self, ev):
        self.clicked.emit()
