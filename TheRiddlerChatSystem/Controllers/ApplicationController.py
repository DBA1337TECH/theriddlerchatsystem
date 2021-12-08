from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject

from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Controllers.MessageController import MessageController
from TheRiddlerChatSystem.Controllers.ReceiveController import ReceiveController
from TheRiddlerChatSystem.Controllers.VillainController import VillainController

from TheRiddlerChatSystem.Model.client import WrappedSocketClient

from threading import Thread
import queue

me = '[ApplicationController]'


class RecvObject(QObject):
    buff_slot = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(RecvObject, self).__init__()


class ApplicationController(BaseController.BaseController ):

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
        self.send_queue = queue.Queue()

        self.courier = WrappedSocketClient
        self.app_obj = RecvObject()
        self.app_obj.buff_slot.connect(self.receive_and_print)
        self.send_button.SendButton.clicked.connect(self.send_message)

        self.thread_c: Thread = Thread(target=self.courier, args=("The_Riddler",
                                                                  "localhost",
                                                                  7272,
                                                                  self.buff_queue,
                                                                  self.app_obj.buff_slot,
                                                                  self.send_queue))
        self.thread_c.start()

    def detected_new_buddy(self):
        pass

    def send_message(self):
        message = self.send_button.ChatMsg.toPlainText()
        if message:
            self.send_queue.put_nowait(message)
            self.send_button.ChatMsg.clear()

    def receive_and_print(self):
        self.villains_list.villains.addItems(self.courier.buddy_list)
        print(f"{me} receive_and_print invoked")
        msg = self.buff_queue.get(True, 1.0)
        if msg:
            print(f"{me} incoming message")
            self.inbox.ChatRecv.addItems([msg])
            msg = None
