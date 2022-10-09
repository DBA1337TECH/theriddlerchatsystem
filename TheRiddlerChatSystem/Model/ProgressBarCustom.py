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


import sys

from PyQt5.QtWidgets import *

sys.path.insert(0, '../Controllers')
sys.path.insert(1, '../Model')
sys.path.insert(2, '../Views')

me = '[ProgressBarCustom]'

class ProgressBarCustom(QProgressBar):

    def __init__(self,view):
        super(ProgressBarCustom, self ).__init__(view)
        self.setGeometry(200,80,250,20)


    def setProgress(self, value):
        print(value)
        self.setValue(value)
