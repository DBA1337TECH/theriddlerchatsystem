"""
DBA 1337_TECH, AUSTIN TEXAS © July 2021
Proof of Concept code, No liabilities or warranties expressed or implied.
"""


import sys, os
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


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
