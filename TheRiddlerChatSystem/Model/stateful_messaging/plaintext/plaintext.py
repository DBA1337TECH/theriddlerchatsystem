from abc import ABC
from typing import List

from chatclient.TheRiddlerChatSystem.Model.stateful_messaging.COM.communication_base import CommunicationBase


class PlainTextCOMM(CommunicationBase):
    def handle_cmd(self, buffer: bytes):
        pass

    def send(self, message: bytes) -> int:
        # TODO
        raise NotImplemented(f"Please finish writing the {self.__class__}  send method")

    def recv(self, buffer: List[bytes]) -> List[bytes]:
        # TODO
        raise NotImplemented(f"Please finish writing the {self.__class__} recv method")
