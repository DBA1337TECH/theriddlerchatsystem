"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
from PySide6.QtWidgets import QWidget

me = '[BaseView]'


class BaseView(QWidget):

    def __init__(self):
        super(BaseView, self).__init__()
        self.components = []

    def initUI(self):
        print(me + 'this is in the Baseview initUI')
        pass
