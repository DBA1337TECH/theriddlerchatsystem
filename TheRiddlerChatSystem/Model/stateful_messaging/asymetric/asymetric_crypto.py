from typing import List

from TheRiddlerChatSystem.Model.stateful_messaging.COM.communication_base import CommunicationBase
from TheRiddlerChatSystem.Model.tools.crypto.CryptoFactory import CryptoFactory


class AsymmetricCryptoMessaging(CommunicationBase):

    def handle_cmd(self, buffer: bytes):
        pass

    def __init__(self, recv_queue, send_queue):
        super().__init__(recv_queue, send_queue)
        self.crypto_tools = CryptoFactory.getCryptoTools("OpenSSL")

    def send(self, message: bytes) -> int:
        """
        send is a method in the asymmetric crypto messaging that should just send the ciphertext bytes

        @param: message is the bytes message object to send
        @returns: an integer of how many bytes were sent
        """
        NotImplemented(f"Please finish writing the {self.__class__} send method")

        return -1

    def recv(self, buffer: List[bytes]) -> List[bytes]:
        """
        recv is a method to receive bytes and order them into a list to be processed.

        @buffer:  is  List of bytes where each element is an incoming message of bytes to be processed.
        """
        NotImplemented(f"Please finish writing the {self.__class__} recv method")

        return [bytes(256), ]
