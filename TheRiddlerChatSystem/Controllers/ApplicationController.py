from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Controllers.MessageController import MessageController
from TheRiddlerChatSystem.Controllers.ReceiveController import ReceiveController
from TheRiddlerChatSystem.Controllers.VillainController import VillainController

from TheRiddlerChatSystem.Model.client import WrappedSocketClient

from threading import Thread

me = '[ApplicationController]'


class ApplicationController(BaseController.BaseController):

    def __init__(self, view, controller_components: list):
        super(ApplicationController, self).__init__(view)
        for controller in controller_components:
            if isinstance(controller, MessageController):
                self.send_button: MessageController = controller
            if isinstance(controller, ReceiveController):
                self.inbox: ReceiveController = controller
            if isinstance(controller, VillainController):
                self.villains_list: VillainController = controller
        self.view = view

        self.courier = WrappedSocketClient
        self.send_button.SendButton.clicked.connect(self.receive_and_print)
        self.thread_c: Thread = Thread(target=self.courier, args=("TheRiddler_DIDITWORK", "localhost", 7272))
        self.thread_c.start()


    def receive_and_print(self):
        self.villains_list.villains.addItems(self.courier.buddy_list)
