#!/usr/bin/env python3
#-*-coding:utf-8-*-
######################

import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET
import pickle
import gzip
import cv2


cam_id = '1'
server_address = ('0.0.0.0', 6666)



def get_camera_frame(cam_id):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(server_address)
    sock.send(b" " * (512 - len(str(cam_id))) + str(cam_id).encode('utf-8'))

    header = sock.recv(512)
    payload_size = int(header.decode('utf-8'))

    data = b""
    while len(data) < payload_size:
        chunk = sock.recv(512)
        if not chunk:
            break
        data += chunk
    sock.close()
    decompressed = gzip.decompress(data)
    iar = pickle.loads(decompressed)
    return iar


cv2.namedWindow(cam_id, cv2.WINDOW_OPENGL)
while True:
    try:
        frame = get_camera_frame(cam_id)
        cv2.imshow(cam_id, frame)
        if cv2.waitKey(1000) == 27:
            break
    except Exception as e:
        print(e)
        break
