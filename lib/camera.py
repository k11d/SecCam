#!/usr/bin/env python3

import cv2
from .viewer import Viewer


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


class MultiStream(object):

    def __init__(self, *cameras):
        self.cameras = list(cameras)
        self.viewer = Viewer(*self.cameras)
        self.cams_fps = {
            cam:cam._fps
            for cam in self.cameras
        }
        self.streams = [
            cam.start_stream()
            for cam in self.cameras
        ]
        self.timings = {
        }

    def close(self):
        for cam in self.cameras:
            cam.close()
        self.viewer.close()

    def update_cam(self, cam_id):
        self.viewer.update_cam(cam_id, self.streams[cam_id].__next__())

    def _fetch_all(self):
        return [[n,self.streams[n].__next__()] for n in range(len(self.cameras))]

    def update_all(self):
        self.viewer.update_all(*self._fetch_all())

