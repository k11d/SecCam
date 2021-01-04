from socket import *
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np
from PIL import Image
import pickle


_pool = ThreadPoolExecutor(10)
_lock = Lock()


def start_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        print("Serving:", addr)
        _pool.submit(handler, client)


def handler(client):
    while True:
        req = client.recv(128)
        sreq = req.decode('utf-8')
        print("Client request:", sreq)
        try:
            with _lock:
                data = fetch_data(int(sreq))
            client.send(data)
        except:
            client.close()
            break


def fetch_data(id):
    if id == 0:
        idata = pickle.dumps(np.array(Image.open('frame_0.png')))
    elif id == 1:
        idata = pickle.dumps(np.array(Image.open('frame_1.png')))
    data = idata + b"\n\n\n\n"
    return data


X = 0
start_server(('0.0.0.0', 6666))