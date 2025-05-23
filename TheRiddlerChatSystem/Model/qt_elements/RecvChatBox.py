"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
import sys

from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListWidget

from TheRiddlerChatSystem.Model.qt_elements.Clickable import ClickMixIn

sys.path.insert(0, '../../Controllers')
sys.path.insert(1, '..')
sys.path.insert(2, '../../Views')


class RecvChatBox(ClickMixIn, QListWidget):
    """
    RecvChatBox is an extension of QTextEdit to allow it to accept the click event
    """
    clickable = Signal()

    def __init__(self, view):
        super(RecvChatBox, self).__init__(view)

    def mousePressEvent(self, mouse_event: QMouseEvent):
        self.clickable.emit()
