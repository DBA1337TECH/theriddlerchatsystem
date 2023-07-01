from abc import ABC, abstractmethod
from typing import List


class CommunicationBase(ABC):

    def __init__(self):
        self.identity = None

    @abstractmethod
    def send(self, message: bytes) -> int:
        raise NotImplemented("Please override the base send method")

    @abstractmethod
    def recv(self, buffer: List[bytes]) -> List[bytes]:
        raise NotImplemented("Please override the abse recv method")
