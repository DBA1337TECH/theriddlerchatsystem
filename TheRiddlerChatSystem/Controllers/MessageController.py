# /usr/env/python3.7
"""
The Riddler Chat System


Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
import os
from PySide6.QtWidgets import QPushButton

from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Model.qt_elements.RecvChatBox import RecvChatBox

me = '[MessageController]'


class MessageController(BaseController.BaseController):

    def __init__(self, view, msg_box, send_button):
        super(MessageController, self).__init__(view)
        self.ChatMsg: RecvChatBox = msg_box
        self.SendButton: QPushButton = send_button
        self.ChatMsg.clickable.connect(self.receive_and_print)
        self.SendButton.clicked.connect(self.send_button_print)
        self.view = view
        self.clicks = 0

    def receive_and_print(self):
        print(me + "clicked a component from the MessageController")

    def send_button_print(self):
        print(me + "SEND THIS SON")
