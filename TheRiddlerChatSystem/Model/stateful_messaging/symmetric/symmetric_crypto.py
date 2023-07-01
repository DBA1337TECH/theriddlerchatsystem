from typing import List

from chatclient.TheRiddlerChatSystem.Model.stateful_messaging.COM.communication_base import CommunicationBase


class SymmetricCryptoMessaging(CommunicationBase)
    def send(self, message: bytes) -> int:
        NotImplemented(f"Please finish writing the {self.__class__} send method")

    def recv(self, buffer: List[bytes]) -> List[bytes]:
        NotImplemented(f"Please finish writing the {self.__class__} recv method")