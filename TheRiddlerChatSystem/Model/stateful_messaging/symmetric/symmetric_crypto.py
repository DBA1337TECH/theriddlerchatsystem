from typing import List

from chatclient.TheRiddlerChatSystem.Model.stateful_messaging.COM.communication_base import CommunicationBase


class SymmetricCryptoMessaging(CommunicationBase)
    def send(self, message: bytes) -> int:
        pass

    def recv(self, buffer: List[bytes]) -> List[bytes]:
        pass