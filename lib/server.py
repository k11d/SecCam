#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import time
import numpy as np
from PIL import Image
import pickle
import sys
import cv2
import os




class Server(object):

    static_test_data = b"HelloWorld"

    def __init__(self, ip_address='0.0.0.0', port=6666):
        self.ip_address, self.port = ip_address, port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.address = (ip_address, port)
        self.sock.bind(self.address)
        self.sock.listen(5)

    def func(self, *args, **kwargs):
        """ should be overwritten by subclass"""
        raise NotImplementedError


    def start(self):
        print(f"Server starting on address: {self.address} - CTRL-C to close.\n")
        while True:
            try:
                client, addr = self.sock.accept()
                print("Serving:", addr)
                self._handler(client)
            except KeyboardInterrupt:
                print("Server shut down")
                break

    def _handler(self, client):
        while True:
            req = client.recv(512)
            sreq = req.decode('utf-8')
            print("Client request:", sreq)
            try:
                # client.send(Server.static_test_data)
                resp = self.func(sreq)
                print("Sending response:", len(resp), " bytes")
                client.send(resp)
            except Exception as e:
                print(e)
            finally:
                print("Done - Closing connection.")
                client.close()
                break

# Example of using the Server class
class ResponseServer(Server):
    def run_os_command(self, cmd):
        return os.popen(cmd).read()

    def func(self, sreq):
        return self.run_os_command(f'figlet "{sreq}"').encode('utf-8')


if __name__ == '__main__':
    s = ResponseServer('0.0.0.0', 6666)
    s.start()
