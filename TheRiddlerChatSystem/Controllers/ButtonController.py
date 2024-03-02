# /usr/env/python3.7
"""
The Riddler Chat System


Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
import os

from PySide6.QtGui import QPixmap
from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Model.Clickable import clickable

from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Model.qt_elements.Clickable import clickable


me = '[ButtonController]'


class ButtonController(BaseController.BaseController):

    def __init__(self, view, component):
        super(ButtonController, self).__init__(view)
        self.checkbox = component
        self.checkbox.clicked.connect(self.changeTitle)
        clickable(self.view.label).connect(self.ClickedTheMap)
        self.view = view
        self.clicks = 0

    def changeTitle(self, state):

        if self.checkbox.isChecked():
            self.view.setWindowTitle('QCheckBox')
        else:
            self.view.setWindowTitle(' ')

    def ClickedTheMap(self):
        self.clicks += 1
        print(self.view.label.curiousposition)