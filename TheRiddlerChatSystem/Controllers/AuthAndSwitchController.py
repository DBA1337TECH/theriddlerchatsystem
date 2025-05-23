"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""

from PySide6.QtCore import Qt

from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Controllers.ApplicationController import ApplicationController
from TheRiddlerChatSystem.Controllers.AuthController import AuthController
from TheRiddlerChatSystem.Views import BaseView
import TheRiddlerChatSystem.Model as DynamicConstants
from TheRiddlerChatSystem.Model.stateful_messaging.mailbox import PostOfficeBox

from queue import Queue


class AuthAndSwitchController(BaseController.BaseController):

    def __init__(self, current_view: BaseView, switch_to_view_success: BaseView = None, ViewSwitcher: BaseController = None):
        super(AuthAndSwitchController, self).__init__(current_view)
        self.view = switch_to_view_success
        self.auth_controller = AuthController(current_view)
        self.current_view = current_view
        self.result = self.auth_controller.result
        self.view_switcher = ViewSwitcher(self.current_view)
        self.current_view.passwordBox.clicked.connect(self.open_application_on_auth)

    def open_application_on_auth(self):
        if self.auth_controller.Authenticate():
            self.view_switcher.HandOffToRiddlerChatSystem()
            if self.view_switcher.view.app is None:
                self.view_switcher.view.app = ApplicationController(self,
                                                                    self.view_switcher.view.controllers,
                                                                    nick_name=self.auth_controller.username)
            self.view_switcher.view.mw.setAttribute(Qt.WA_TranslucentBackground, False)
            print("Successful view switch to the Riddler Chat Application")

        else:
            print("Did not Authenticate")
