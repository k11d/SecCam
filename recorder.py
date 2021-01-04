#!/usr/bin/env python3

import cv2
import numpy as np
import glob
import os

class Recorder(object):
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self._video_writer = None

    def __enter__(self):
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        self._video_writer = cv2.VideoWriter("output.avi", fourcc, self.fps, (self.width, self.height))
        return self
    def __exit__(self, ex, ec, etb):
        self._video_writer.release()

    def write(self, frame):
        self._video_writer.write(frame)

    @classmethod
    def from_image_sequence(cls, dirpath):
        def _list_images():
            return (f
                for f in
                (
                    glob.glob(dirpath + f'/*.{ext}')
                    for ext in ('jpg', 'png')
                )
            )
        def _get_alpha_mask(img):
            mask = np.zeros_like(img[:,:,:3], dtype=img.dtype)
            mask.fill(0)
            transparent = img[:,:,-1] <= 1
            mask[transparent, 0] = 0
            mask[transparent, 1] = 0
            mask[transparent, 2] = 0
            return mask

        images = sorted([f
            for g in _list_images()
            for f in g],
            key=lambda fpath: os.path.basename(fpath),
            reverse=True
        )

        print(f"reading from {len(images)} image frames")
        frame = cv2.imread(images.pop(), cv2.IMREAD_UNCHANGED).astype(np.uint8)
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        alpha_mask = _get_alpha_mask(frame)
        bgr_frame = np.bitwise_and(bgr_frame, alpha_mask)

        height, width = frame.shape[:2]
        bg = np.ndarray(shape=(height, width, 3), dtype=frame.dtype)
        bg.fill(255)
        with cls(width, height, 25) as rec:
            rec.write(bg)
            while frame is not None:
                rec.write(bgr_frame)
                try:
                    f = images.pop()
                    frame = cv2.imread(f)
                    bgr_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    alpha_mask = _get_alpha_mask(frame)
                    bgr_frame = np.bitwise_and(bgr_frame, alpha_mask)
                except:
                    frame = None
        print('Done')


if __name__ == '__main__':
    # Recorder.from_image_sequence('/home/kid/Bureau/cc')
    import sys
    src = cv2.VideoCapture(sys.argv[1])
    with Recorder(1280, 720, 18) as rec:
        for _ in range(500):
            ret, frame = src.read()
            if ret:
                rec.write(frame)


