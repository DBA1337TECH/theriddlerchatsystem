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
