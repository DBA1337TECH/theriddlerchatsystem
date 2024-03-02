
"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
from TheRiddlerChatSystem.Controllers import BaseController
from TheRiddlerChatSystem.Model.qt_elements.VillainList import VillainList


me = '[VillainController]'


class VillainController(BaseController.BaseController):

    def __init__(self, view, component):
        super(VillainController, self).__init__(view)
        self.villains: VillainList = component
        self.villains.clickable.connect(self.receive_and_print)
        self.view = view
        self.clicks = 0

    def receive_and_print(self):
        print(me + "clicked the List Box from VillainController")
