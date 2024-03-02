"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""

from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListWidget


class VillainList(QListWidget):
    """
    VillainList identical to a buddy list
    """
    clickable = Signal()

    def __init__(self, view):
        super(VillainList, self).__init__(view)

    def mousePressEvent(self, mouse_event: QMouseEvent):
        self.clickable.emit()
