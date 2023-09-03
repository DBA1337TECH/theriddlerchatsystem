"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QListWidget


class VillainList(QListWidget):
    """
    VillainList identical to a buddy list
    """
    clickable = pyqtSignal()

    def __init__(self, view):
        super(VillainList, self).__init__(view)

    def mousePressEvent(self, mouse_event: QMouseEvent):
        self.clickable.emit()
