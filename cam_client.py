#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET
import pickle
import gzip
from PIL import Image

cam_id = '0'
server_address = ('0.0.0.0', 6666)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(server_address)
sock.send(str(cam_id).encode('utf-8') + b" " * 511)

data = b""
while True:
    chunk = sock.recv(512)
    if not chunk:
        break
    data += chunk
sock.close()
decompressed = gzip.decompress(data)
iar = pickle.loads(decompressed)
Image.fromarray(iar).show()

