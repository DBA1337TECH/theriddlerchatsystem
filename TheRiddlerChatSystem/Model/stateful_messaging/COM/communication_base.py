"""
DBA 1337_TECH, AUSTIN TEXAS © July 2021
Proof of Concept Proprietary code, No liabilities or warranties expressed or implied.
All Rights Reserved by 1337_TECH, DBA held in AUSTIN TEXAS
"""
import re
from abc import ABC, abstractmethod
from queue import Queue
from socket import socket
from typing import List, ByteString
from chatclient.TheRiddlerChatSystem.Model.buddy_list.BuddyList import BuddyList
from chatclient.TheRiddlerChatSystem.Model.Constants import BuddyList



class CommunicationBase(ABC):

    def __init__(self, send_queue: Queue, recv_queue: Queue):
        self.identity = None
        self.parse_and_build: CommandParserAndBuilder = CommandParserAndBuilder()
        self.send_queue = None
        self.recv_queue = None
        self._init(send_queue, recv_queue)
        self.buddy_list_obj:BuddyList = BuddyList

    def _init(self, send_queue, recv_queue):
        self._init_recv_queue(recv_queue)
        self._init_send_queue(send_queue)

    def _init_recv_queue(self, recv_queue: Queue) -> bool:
        try:
            self.recv_queue: Queue = recv_queue
            return True
        except TypeError as e:
            return False

    def _init_send_queue(self, send_queue: Queue) -> bool:
        try:
            self.send_queue: Queue = send_queue
            return True
        except TypeError as e:
            return False

    @abstractmethod
    def send(self, message: bytes) -> int:
        raise NotImplemented("Please override the base send method")

    @abstractmethod
    def recv(self, buffer: List[bytes]) -> List[bytes]:
        raise NotImplemented("Please override the base recv method")

    @abstractmethod
    def handle_cmd(self, buffer: bytes):
        raise NotImplemented("Please override the base handle_cmd method")

    def client_Thread_Send(self, client_socket: socket = None):
        while True:
            message = f"{self.send_queue.get(True)}"
            try:
                self.buddy_list_obj.buddy_list_lock.acquire()
                for screen_name, identity in self.buddy_list_obj.buddy_list.items():
                    client_socket.sendto(self.parse_and_build.commands_send[b'MESG'] + self.nick.encode() + b':'
                                         + message.encode() + b'\n', identity)
            except Exception as e:
                print(e)
            finally:
                self.buddy_list