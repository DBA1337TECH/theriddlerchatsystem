import sys

from PyQt5.QtCore import pyqtSignal
# from StenographyController import StenographyController
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTextEdit

from TheRiddlerChatSystem.Model.Clickable import ClickMixIn

sys.path.insert(0, '../Controllers')
sys.path.insert(1, '../Model')
sys.path.insert(2, '../Views')


class RecvChatBox(ClickMixIn, QTextEdit):
    clickable = pyqtSignal()

    def __init__(self, name, view):
        super(RecvChatBox, self).__init__(name, view)

    def mousePressEvent(self, mouse_event: QMouseEvent):
        self.clickable.emit()
