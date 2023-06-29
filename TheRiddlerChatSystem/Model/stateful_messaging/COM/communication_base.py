from abc import ABC, abstractmethod
from typing import List


class CommunicationBase(ABC):

    def __init__(self):
        self.identity = None

    @abstractmethod
    def send(self, message: bytes) -> int:
        pass

    @abstractmethod
    def recv(self, buffer: List[bytes]) -> List[bytes]:
        pass