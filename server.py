# server.py

import socket
import sys
from io import BytesIO
from PIL import Image


def start_server(address=('0.0.0.0', 6666)):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('starting up on {} port {}'.format(*address))
    sock.bind(address)
    return sock


def listen(sock):
    sock.listen(1)
    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        handle_client(connection, client_address, server_task)


def server_task():
    return b"HelloWorld"


def handle_client(connection, address, task, keep_alive=False):
    data = bin()
    while True:
        try:
            print('connection from', address)
            while True:
                chunk = connection.recv(16)
                if chunk:
                    print('received {!r}'.format(chunk))
                    #connection.sendall(data)
                    data += chunk
                else:
                    print('no data from', address)
                    break
        finally:
            if not keep_alive:
                connection.close()
            # if data:
            #     data = BytesIO(_data).read()
                outname = 'data_' + address + '.png'
                with open(outname, 'wb') as f:
                    f.write(data)



def run():
    s = start_server()
    listen(s)

run()

