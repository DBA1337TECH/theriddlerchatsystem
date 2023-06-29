import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTextEdit

from chatclient.TheRiddlerChatSystem.Model.Clickable import ClickMixIn

sys.path.insert(0, '../Controllers')
sys.path.insert(1, '../Model')
sys.path.insert(2, '../Views')


class MsgChatBox(ClickMixIn, QTextEdit):
    """
    MsgChatBox is an extension of QTextEdit to allow it to accept the click event
    """
    clickable = pyqtSignal()

    def __init__(self, name, view):
        super(MsgChatBox, self).__init__(name, view)

    def mousePressEvent(self, mouse_event: QMouseEvent):
        self.clickable.emit()
