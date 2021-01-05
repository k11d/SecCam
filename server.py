#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from socket import *
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
from PIL import Image
import pickle
from threading import Lock
import sys
import cv2
import os



_pool = ProcessPoolExecutor(10)
_lock = Lock()


class Server(object):
    
    static_test_data = b"HelloWorld"

    def __init__(self, ip_address='0.0.0.0', port=6666):
        self.ip_address, self.port = ip_address, port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((ip_address, port))
        self.sock.listen(5)

    def start(self):
        while True:
            client, addr = self.sock.accept()
            print("Serving:", addr)
            self._handler(client)


    def _handler(self, client):
        while True:
            req = client.recv(512)
            sreq = req.decode('utf-8')
            print("Client request:", sreq)
            try:
                # client.send(Server.static_test_data)
                client.send(self.figletizer(sreq).encode('utf-8'))
            except Exception as e:
                print(e)
            finally:
                client.close()
                break
    
    def run_os_command(self, cmd):
        return os.popen(cmd).read()


    def figletizer(self, s):
        return self.run_os_command(f"figlet {s}")


s = Server('0.0.0.0', 6666)
s.start()
