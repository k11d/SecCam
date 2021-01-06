#!/usr/bin/env python3

import pickle
import gzip
from lib.server import Server
from lib.camera import Camera, MultiStream



class CamServer(Server):
    def func(self, sreq):
        if sreq.strip() == '0':
            return gzip.compress(pickle.dumps(s0.__next__()))
        elif sreq.strip() == '1':
            return gzip.compress(pickle.dumps(s1.__next__()))
        else:
            return b""


s0 = Camera('/dev/video1').start_stream()
s1 = Camera('/dev/video3').start_stream()
cs = CamServer()
cs.start()

