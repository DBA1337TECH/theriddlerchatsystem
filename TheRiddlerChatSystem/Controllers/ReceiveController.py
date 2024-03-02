# /usr/env/python3.7

"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""

from TheRiddlerChatSystem.Model.qt_elements.RecvChatBox import RecvChatBox

from TheRiddlerChatSystem.Controllers import BaseController

me = '[ReceiveController]'


class ReceiveController(BaseController.BaseController):

    def __init__(self, view, component):
        super(ReceiveController, self).__init__(view)
        self.ChatRecv: RecvChatBox = component
        self.ChatRecv.clickable.connect(self.receive_and_print)
        self.view = view
        self.clicks = 0

    def receive_and_print(self):
        print(me + "clicked the Receive Chat Box from ReceiveController")


