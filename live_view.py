#!/usr/bin/env python3

import cv2
from lib.camera import Camera, MultiStream
from lib.processing import ImageProcessing
import pickle



class LiveViewer(object):

    def __init__(self, *cameras):
        self.ms = MultiStream(*cameras)
        self.ip = ImageProcessing()
        self.quit = False

    def keyboard_event_handler(self):
        k = cv2.waitKey(1)
        if k == 27:
            self.quit = True
            self.ms.close()

        elif k == ord('t'):
            self.ip.toggle_threshold = not self.ip.toggle_threshold
        elif k == ord('g'):
            self.ip.toggle_grayscale = not self.ip.toggle_grayscale
        elif k == ord('g'):
            self.ip.toggle_grayscale = not self.ip.toggle_grayscale
        elif k == ord('f'):
            self.ip.toggle_face_detection = not self.ip.toggle_face_detection
        elif k == ord('z'):
            self.ip.threshold_limit -= self.ip.threshold_delta
        elif k == ord('u'):
            self.ip.threshold_limit += self.ip.threshold_delta

    def run(self):
        while not self.quit:
            self.ms.update_cam(0)
            self.ms.update_cam(1)
            self.keyboard_event_handler()

if __name__ == '__main__':
    lv = LiveViewer(
        Camera('/dev/video1'),
        Camera('/dev/video3')
    )
    lv.run()

