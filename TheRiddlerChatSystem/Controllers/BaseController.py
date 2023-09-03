# /usr/env/python3.7
"""
The Riddler Chat System

Author: 1337_TECH DBA. Austin Texas
DATE: 03/04/2022
Updated: 10/09/2022
client.py for Riddler Chat System
"""
from TheRiddlerChatSystem.Views import BaseView

me = '[BaseController]'


class BaseController(object):

    def __init__(self, view):
        self.components = []

        if isinstance(view, BaseView.BaseView):
            self.view = view
        else:
            self.view = None
            print(me + 'ERROR>We are not a BaseView')

    def ActiveListener(self):
        print('called from the Base controller')
