#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import socket
from PIL import Image
import numpy as np
from io import BytesIO
import random
import time
import pickle



def _try_import_opencv():
    try:
        import cv2
    except ImportError:
        return False
    else:
        cv2.namedWindow(str(device_id), cv2.WINDOW_GUI_NORMAL)
        return True


def show(frame):
    cv2.imshow(str(device_id), frame)
    if cv2.waitKey(2) == 27:
        cv2.destroyAllWindows()
        sys.exit(0)


device_id = sys.argv[1]
_show = _try_import_opencv()
if _show:
    import cv2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0', 6666)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
connected = True
data = b""
while connected:
    # device_id = 0 if random.random() < 0.5 else 1
    sock.send(str(device_id).encode('utf-8') + b" " * 127)
    while not b"\n\n\n\n" in data:
        try:
            chunk = sock.recv(512)
            if chunk:
                data += chunk
            else:
                print("no data")
                break
        except:
            print("Lost server connection")
            connected = False
            break
    if not data.endswith(b"\n\n\n\n"):
        sep = data.find(b"\n\n\n\n")
        tmp = data[:sep]
    try:
        img = pickle.loads(data[:-4])
        if _show:
            show(img)
    except Exception as e:
        print(e)
    finally:
        data = data[sep+3:]
        time.sleep(2)
sock.close()
