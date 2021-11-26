from PyQt5.QtCore import Qt

from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Controllers.AuthController import AuthController
from TheRiddlerChatSystem.Views import BaseView


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
        if self.auth_controller.result:
            self.view_switcher.HandOffToRiddlerChatSystem()
            self.view_switcher.view.mw.setAttribute(Qt.WA_TranslucentBackground, False)
            print("successful view switch to the Riddler Chat Application")
