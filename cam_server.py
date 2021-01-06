#!/usr/bin/env python3
#-*-coding:utf-8-*-

import pickle
import gzip
from lib.server import Server
from lib.camera import Camera, MultiStream
from lib.image_utils import resize, grayscale
import cv2



class CamServer(Server):
    def func(self, sreq):
        if sreq.strip() == '0':
            iar = grayscale(resize(s0.__next__(), (320, 240)))
            return gzip.compress(pickle.dumps(iar))
        elif sreq.strip() == '1':
            iar = grayscale(resize(s1.__next__(), (320, 240)))
            return gzip.compress(pickle.dumps(iar))
        else:
            return b""


s0 = Camera('/dev/video1').start_stream()
s1 = Camera('/dev/video3').start_stream()
cs = CamServer()
cs.start()

