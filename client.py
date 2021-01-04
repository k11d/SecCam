# client.py

import sys
import socket
from PIL import Image
import numpy as np


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('172.22.22.65', 9999)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# send command
data = np.array(Image.open(sys.argv[1])).tobytes()
sock.sendall(data)

# amount_received = 0
# amount_expected = len(message)

ak = int(sock.recv(64))
print('received:', ak)
sock.close()