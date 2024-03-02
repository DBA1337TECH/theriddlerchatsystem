"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
import socket

from PySide6.QtCore import Slot, Signal, QObject
from queue import Queue
from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Controllers.MessageController import MessageController
from TheRiddlerChatSystem.Controllers.ReceiveController import ReceiveController
from TheRiddlerChatSystem.Controllers.VillainController import VillainController

from TheRiddlerChatSystem.Model.client import WrappedSocketClient
from TheRiddlerChatSystem.Model.stateful_messaging.mailbox import PostOfficeBox
from TheRiddlerChatSystem.Model.stateful_messaging.COM.communication_base import CommunicationBase
from TheRiddlerChatSystem.Model.stateful_messaging.plaintext.plaintext import PlainTextCOMM
from TheRiddlerChatSystem.Model.Constants import buddy_list_obj

from threading import Thread
import queue

me = '[ApplicationController]'


class RecvObject(QObject):
    buff_slot = Signal(object)

    def __init__(self, *args, **kwargs):
        super(RecvObject, self).__init__()


class ApplicationController(BaseController.BaseController):

    def __init__(self, view, controller_components: list, nick_name: str):
        super(ApplicationController, self).__init__(view)
        for controller in controller_components:
            if isinstance(controller, MessageController):
                self.send_button: MessageController = controller
            if isinstance(controller, ReceiveController):
                self.inbox: ReceiveController = controller
            if isinstance(controller, VillainController):
                self.villains_list: VillainController = controller
        self.view = view

        self.po_box: PostOfficeBox = PostOfficeBox(Queue(100), Queue(100))
        self.po_box.nick_name = nick_name
        self.buff_queue = Queue(200)
        self.send_queue = self.po_box.send_udp_queue
        self.recv_queue = self.po_box.recv_udp_queue

        self.courier: WrappedSocketClient = WrappedSocketClient
        self._comms_state: CommunicationBase = PlainTextCOMM(self.po_box.send_udp_queue,
                                                             self.po_box.recv_udp_queue,
                                                             socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                                                             socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                                                             buff_queue=self.buff_queue)
        self.app_obj = RecvObject()
        self.app_obj.buff_slot.connect(self.receive_and_print)
        self.send_button.SendButton.clicked.connect(self.send_message)

        self.thread_c: Thread = Thread(target=self.courier, args=(f"{self.po_box.nick_name}",
                                                                  "localhost",
                                                                  7272,
                                                                  self._comms_state.recv_queue,
                                                                  # may need to change to recv queue in the future
                                                                  self.app_obj.buff_slot,
                                                                  self._comms_state.send_queue))
        self.thread_c.start()

    def detected_new_buddy(self):
        pass

    def send_message(self):
        message = self.send_button.ChatMsg.toPlainText()
        if message:
            self.send_queue.put_nowait(message)
            self.send_button.ChatMsg.clear()

    def receive_and_print(self):
        self.villains_list.villains.clear()
        self.villains_list.villains.addItems(buddy_list_obj.buddy_list)
        print(f"{me} receive_and_print invoked")
        try:
            msg = self.recv_queue.get(True, 1.0)
        except queue.Empty as e:
            print("queue has already been processed?")
            msg = None
        if msg:
            print(f"{me} incoming message")
            self.inbox.ChatRecv.addItems([msg])
            msg = None
