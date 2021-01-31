"""
Author: Blake D. De Garza
UTEID: bd6225
DATE: 01/16/2021

Object Oriented client for Lab2
"""
import argparse
import re
import socket
from _thread import start_new_thread
import random
from threading import Lock
from typing import ByteString


class CommandParserAndBuilder:
    """
    CommandParserAndBuilder initializes dictionaries that make it convenient to parse and build messages for Lab2 of
    Communication and Networks: Tech/Arch/Protocol
    """

    def __init__(self):
        # format will be tuple of command and keyword arguments
        self.commands_send = {
            b'HELO': (b'HELO', ['screen_name', 'ip', 'port']),
            b'MESG': (b'MESG ', ['screen_name', 'message']),
            b'EXIT': b'EXIT\n',
        }

        self.commands_recv = {
            b'JOIN': (b'JOIN ', ['screen_name', 'ip', 'port']),
            b'MESG': (b'MESG ', ['screen_name', 'message']),
            b'EXIT': (b'EXIT ', ['screen_name']),
            b'ACPT': (b'ACPT ', ['screen_name', 'ip', 'port']),
            b'RJCT': (b'RJCT', ['screen_name']),
        }

        self.parser_mux_recv = {
            b'JOIN': self.join_handle_recv,
            b'MESG': self.mesg_handle_recv,
            b'EXIT': self.exit_handle_recv,
            b'ACPT': self.acpt_handle_recv,
        }

        self.parser_mux_send = {
            b'MESG': self.mesg_send,
        }

    @staticmethod
    def join_handle_recv(**kwargs) -> str:
        """ receives the RECV command and handles as neccesary"""
        screen_name = "screen_name"
        result = f"{kwargs[screen_name]} has entered the room"
        print(result)
        return result

    @staticmethod
    def mesg_handle_recv(**kwargs) -> str:
        """ receives the MESG command and handles as neccesary"""
        message = 'message'
        screen_name = 'screen_name'
        # now go into the builder and build the actual format string
        message_builder = f"{kwargs[screen_name]}: {kwargs[message]}"
        return message_builder

    @staticmethod
    def exit_handle_recv(**kwargs) -> str:
        """ receives the EXIT command and handles as neccesary"""
        screen_name = 'screen_name'
        return f'{kwargs[screen_name]} has left the room\n'

    @staticmethod
    def acpt_handle_recv(**kwargs):
        """ receives the ACPT command and handles as neccesary"""
        pass

    @staticmethod
    def rejct_handle_recv(**kwargs) -> str:
        """ recieves the REJCT command meaning the screen_name already exists"""
        screen_name = 'screen_name'
        return f'{kwargs[screen_name]} is already in use please choose another one'

    @staticmethod
    def exit_send(**kwargs) -> ByteString:
        return b'EXIT\n'

    @staticmethod
    def mesg_send(**kwargs) -> ByteString:
        screen_name = 'screen_name'
        message = 'message'
        result = F"MESG {kwargs[screen_name]}: {kwargs[message]}\n".encode()
        print(f"THIS IS WHAT WE ARE SENDING: {result}")
        return result


class WrappedSocketClient:
    """
    WrappedSocket aims to take in only the needed parameters and create a TLS protocol SSL wrapped socket using only
    """
    end_of_command = b'\n'
    commands_send = {
        b'HELO': b'HELO ',
        b'MESG': b'MESG ',
        b'EXIT': b'EXIT\n',
        b'ACPT': b'ACPT '
    }

    commands_recv = {
        b'JOIN': b'JOIN ',
        b'MESG': b'MESG ',
        'EXIT': b'EXIT ',
        b'ACPT': b'ACPT ',
    }

    buddy_list = {}  # fill in order of {nick_name:(ip, port),}
    buddy_list_lock = Lock()
    parse_and_build = CommandParserAndBuilder()

    def __init__(self, nickname: str, ip: str, server_port: int):
        self.nick = nickname
        self.hostname = ip
        self.port = server_port
        try:
            self.registration()
        except Exception as e:
            print(e)
            exit()

        # use Object Oriented Design
        self.socket_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create our TCP socket used for
        self.socket_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create our UDP socket
        # initialization

        # Establishment of UDP and TCP
        self.udp_port = random.randint(self.port, 2 ** 16 - 1)
        self.socket_UDP.bind((self.hostname, self.udp_port))
        connection_str = self.commands_send[b'HELO'] + self.nick.encode() + b' ' + self.hostname.encode() \
                         + b' ' + (str(self.udp_port)).encode() + self.end_of_command

        self.socket_TCP.connect((self.hostname, self.port))

        # 2
        self.socket_TCP.send(connection_str)

        self.client_Thread_Start()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Closing Time, Time for the last Call...")
        print("Ouch it's closed")

    def registration(self):
        # self.nick = str((input("Please enter your nickname:>").split(':>')[0]))
        # print(self.nick)
        # self.hostname = str((input("Please give us your IP:>").split(':>')[0]))
        # print(self.hostname)
        # self.port = int(input("Please give us the port of the Server:>").split(":>")[0])
        # print(self.port)

        # Sanity Checks before connection to server
        if not self.check_for_correct_ip() and self.hostname != "localhost":
            print("ERROR INCORRECT FORMAT IDENTIFIER IP")
            raise Exception("Cannot move forward as the ip address is not of correct format %2x.%2x.%2x.%2x format")

        if not isinstance(self.port, int):
            print("port is not a integer")
            raise Exception("port is not an integer")

        if self.port > 2 ** 16 or self.port <= 0:
            print("port number is out of range")
            raise Exception("port is out of range")

        if self.nick.find(' ') >= 0:
            print("nickname cannot include ASCII spaces")
            raise Exception("nickname has a space")

    def check_for_correct_ip(self) -> bool:
        regex_compile = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        x = regex_compile.match(self.hostname)
        if x:
            result = True
        else:
            result = False

        return result

    def client_Thread_Start(self, clientSocket: socket = None):
        start_new_thread(self.client_Thread_Send, (self.socket_UDP,), )
        start_new_thread(self.client_Thread_Read, (self.socket_UDP,), )
        start_new_thread(self.client_Thread_TCP, (self.socket_TCP,), )

    def client_Thread_Send(self, clientSocket: socket = None):
        while True:
            message = input("send:>").split(':>')[0]
            try:
                self.buddy_list_lock.acquire()
                for screen_name, identity in self.buddy_list.items():
                    print(f"SENDING MESSAGE {message}")
                    clientSocket.sendto(self.commands_send[b'MESG'] + self.nick.encode() + b':'
                                        + message.encode() + b'\n', identity)
            except Exception as e:
                print(e)
            finally:
                self.buddy_list_lock.release()

    def client_Thread_TCP(self, clientSocket: socket = None):
        while True:
            full_command = b''
            # read in a message from the Read Thread
            while full_command.find(b'\n') == -1:
                full_command += clientSocket.recv(1048)

            # parse that message
            full_command = (re.sub(b'.\n|:', b' ', full_command)).split(b' ')
            # full_command.reverse()
            # a part of parsing make sure it's a valid command before we parse
            handle = self.parse_and_build.parser_mux_recv[full_command[0]]

            if handle:
                keyword_args = self.parse_and_build.commands_recv[full_command[0]][1]
                arguments = {}
                full_command.reverse()
                cmd = full_command.pop()
                full_command = full_command[1:]
                while len(full_command) > 1:
                    if cmd != b'ACPT':
                        for key in keyword_args:
                            arguments[key] = full_command.pop()
                    else:
                        # full_command.reversed()
                        print("THIS IS THE FULLCOMMAND: " + str(full_command))
                        self.buddy_list_lock.acquire()
                        try:
                            screen_name = full_command.pop()
                            ip = full_command.pop()
                            port = full_command.pop()
                            self.buddy_list[screen_name] = (str(ip.decode()),
                                                            int(str(port.decode())))
                        except Exception as e:
                            print(e)
                        finally:
                            print("THIS IS THE BUDDY LIST IN Thread Read:" + str(self.buddy_list))
                            self.buddy_list_lock.release()
                            continue
                        # screen_name = full_command.pop()
                        # ip = full_command.pop()
                        # port = full_command.pop()
                        # self.buddy_list_lock.acquire()
                        # try:
                        #     self.buddy_list[screen_name] = (ip.decode(), int(port.decode()))
                        # finally:
                        #     print("THIS IS THE BUDDY LIST:" + str(self.buddy_list))
                        #     self.buddy_list_lock.release()

    def client_Thread_Read(self, clientSocket: socket = None):
        while True:
            full_command = b''
            # read in a message from the Read Thread
            while full_command.find(b'\n') == -1:
                full_command += clientSocket.recvfrom(1048)[0]

            # parse that message
            if self.commands_recv[b'MESG'][0] in full_command:
                full_command = (re.sub(b'.\n|:', b' ', full_command)).split(b' ')
                full_command.reverse()
                # a part of parsing make sure it's a valid command before we parse
                handle = self.parse_and_build.parser_mux_recv[full_command[-1]]

            elif self.commands_recv[b'ACPT'][0] in full_command:
                full_command = re.sub(b'\n', b'', full_command)
                print("THIS IS THE FULLCOMMAND: " + str(full_command))
                full_command.replace(b'ACPT ', b'')
                # full_command = b':'.join(full_command)
                parse_full_command = full_command.split(b':')
                self.buddy_list_lock.acquire()
                try:
                    self.buddy_list[parse_full_command.pop()] = (str(parse_full_command.pop()),
                                                                 int(str(parse_full_command.pop())))
                finally:
                    print("THIS IS THE BUDDY LIST IN Thread Read:" + str(self.buddy_list))
                    self.buddy_list_lock.release()
                    continue

            elif self.commands_recv[b'JOIN'][0] in full_command:
                full_command.replace(b'JOIN ', b'')

                pop_full_command = full_command.split(b' ')
                self.buddy_list_lock.acquire()
                try:
                    self.buddy_list[pop_full_command.pop()] = (str(pop_full_command.pop()),
                                                               int(str(pop_full_command.pop())))
                finally:
                    print("THIS IS THE BUDDY LIST IN Thread Read:" + str(self.buddy_list))
                    self.buddy_list_lock.release()
                    continue
            else:
                full_command = (re.sub(b'\n', b'', full_command)).split(b' ')
                full_command.reverse()
                # a part of parsing make sure it's a valid command before we parse
                handle = self.parse_and_build.parser_mux_recv[full_command[-1]]

            if handle:
                keyword_args = self.parse_and_build.commands_recv[full_command[-1]][1]
                arguments = {}
                cpy_command = full_command.copy()
                cmd = full_command.pop()
                while len(full_command) > 1:
                    if cmd != b'ACPT':
                        for key in keyword_args:
                            arguments[key] = full_command.pop()
                        arguments['full_message'] = cpy_command
                    else:
                        pass

                response = b''

                if cmd != b'ACPT' and cmd:
                    response = handle(**arguments)

                if response:
                    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('nickname', metavar='nickname', type=str,
                        help='Chatter Arguments are in form client.py <nickname> <ip> <server_port>')
    parser.add_argument('ip', metavar='ip', type=str)
    parser.add_argument('server_port', metavar='server_port', type=int)
    args = parser.parse_args()

    if isinstance(args.nickname, str) and isinstance(args.ip, str) and isinstance(args.server_port, int):
        client = WrappedSocketClient(args.nickname, args.ip, args.server_port)
    else:
        print("Your arguments are off")
        exit()
