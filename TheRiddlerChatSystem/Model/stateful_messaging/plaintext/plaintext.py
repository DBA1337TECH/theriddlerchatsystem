from abc import ABC
from typing import List

from chatclient.TheRiddlerChatSystem.Model.stateful_messaging.COM.communication_base import CommunicationBase

class PlainTextCOMM(CommunicationBase):
    def send(self, message: bytes) -> int:
        #TODO

    def recv(self, buffer: List[bytes]) -> List[bytes]:
        #TODO