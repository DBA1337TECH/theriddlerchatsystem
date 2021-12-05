from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Controllers.MessageController import MessageController
from TheRiddlerChatSystem.Controllers.ReceiveController import ReceiveController
from TheRiddlerChatSystem.Controllers.VillainController import VillainController

from TheRiddlerChatSystem.Model.client import WrappedSocketClient

from threading import Thread
import queue

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

        self.buff_queue = queue.Queue()
        self.courier = WrappedSocketClient
        self.send_button.SendButton.clicked.connect(self.receive_and_print)
        self.thread_c: Thread = Thread(target=self.courier, args=("TheRiddler_DIDITWORK",
                                                                  "localhost",
                                                                  7272,
                                                                  self.buff_queue))
        self.thread_c.start()


    def receive_and_print(self):
        self.villains_list.villains.addItems(self.courier.buddy_list)
        print("WE RECIEVED A MESSAGE")
        self.inbox.ChatRecv.addItem("HARLEY_QUINN: We Hacking?!?!")
        msg = self.buff_queue.get(True, 1.0)
        if msg:
            print(f"{me} incoming message")
            self.inbox.ChatRecv.addItems([msg])
            msg = None

