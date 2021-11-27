"""
DBA 1337_TECH, AUSTIN TEXAS © July 2021
Proof of Concept code, No liabilities or warranties expressed or implied.
"""
from TheRiddlerChatSystem.Controllers.AuthAndSwitchController import AuthAndSwitchController
from TheRiddlerChatSystem.Controllers.ViewSwitcher import ViewSwitcher
from TheRiddlerChatSystem.Views.LandingPage import LandingPage
from TheRiddlerChatSystem.Views.MainWindow import MainWindow

'''
Although it is titled the Landing page it is being treated more like the initial
Setup.  Luckily this is just a view so it is subject to change, the Developer can
always make a view called GameBoard (as an example) which inherits the BaseView
'''

import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from TheRiddlerChatSystem.Controllers.AuthController import AuthController
from TheRiddlerChatSystem.Model.CustomLabel import LoadingLabel
from TheRiddlerChatSystem.Model.TextBoxes import SecretTextBox


from TheRiddlerChatSystem.Views import BaseView
from TheRiddlerChatSystem.Model.CustomLabel import *


class AuthenticateView(BaseView.BaseView):

    def __init__(self, window: MainWindow = None):
        super(AuthenticateView, self).__init__()
        self.ctrl = None
        self.components = []
        self.p = None
        self.p2 = None
        self.mw = window
        self.controller = None

        self.initUI()

    def initUI(self):
        self.p = QPixmap(os.getcwd() + '/images/DarkKnight_logo.png')
        self.logo = QPixmap(os.getcwd() + '/images/1337_TECH_NEW_LOGO.png')
        hbox = QHBoxLayout(self)

        self.main_label = LoadingLabel(alignment=Qt.AlignCenter)
        self.main_label.setPixmap(self.p)
        self.main_label.setAttribute(Qt.WA_TranslucentBackground, True)

        self.passwordBox = SecretTextBox(self.main_label, text='password')
        self.usernameBox = SecretTextBox(self.main_label, text='username')
        self.usernameBox.move(self.main_label.size().width() + 50, 200)
        self.usernameBox.setStyleSheet('background-color: rgb(244,40,40); border-radius: 10;')

        self.passwordBox.setEchoMode(QLineEdit.Password)
        self.passwordBox.setStyleSheet('background-color: rgb(244,40,40); border-radius: 10;')
        self.passwordBox.move(self.main_label.size().width() + 50, 300)

        self.usernameBox.setFont(QFont("Helvetica", 14, QFont.ExtraBold))

        hbox.addWidget(self.main_label)

        # self.viewswitch_controller: ViewSwitcher = ViewSwitcher(self, LandingPage)
        self.controller: AuthAndSwitchController = AuthAndSwitchController(self, LandingPage, ViewSwitcher)

        # self.passwordBox.clicked.connect(self.controller.auth_controller.Authenticate)

        # self.show()
