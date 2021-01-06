#!/usr/bin/env python3

import cv2


class Camera(object):
    def __init__(self, device=0, delay_capture=False):
        self.device = device 
        self._cap = None
        if not delay_capture:
            self.capture()

    def capture(self):
        if self._cap is None:
            self._cap = cv2.VideoCapture(self.device)
            self._fps = self._cap.get(cv2.CAP_PROP_FPS)
            self._height = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self._width = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self._frame_count = self._cap.get(cv2.CAP_PROP_FRAME_COUNT)
            print(self.device, self._fps, self._height, self._width, self._frame_count)

    def start_stream(self):
        while True:
            frame = self.read()
            yield frame
            
    def close(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def read(self):
        _, frame = self._cap.read()
        return frame
