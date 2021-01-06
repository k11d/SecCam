import cv2
from camera import Camera
from lib.processing import ImageProcessing



class MultiStream(object):

    def __init__(self, *cameras):
        self.cameras = list(cameras)
        self.cams_fps = {
            cam:cam._fps
            for cam in self.cameras
        }
        self.streams = [
            cam.start_stream()
            for cam in self.cameras
        ]
    def close(self):
        for cam in self.cameras:
            cam.close()


def run(*cameras):

    ms = MultiStream(*cameras)

    for n, cam in enumerate(ms.cameras):
        cv2.namedWindow(str(n), cv2.WINDOW_GUI_NORMAL)
        cv2.setWindowTitle(str(n), cam.device)

    ip = ImageProcessing()

    while True:
        for n, frame in enumerate(map(ip.apply_all, map(next, ms.streams))):
            cv2.imshow(str(n), frame)
        k = cv2.waitKey(1)
        if k == 27:
            ms.close()
            cv2.destroyAllWindows()
            break
        elif k == ord('t'):
            ip.toggle_threshold = not ip.toggle_threshold
        elif k == ord('g'):
            ip.toggle_grayscale = not ip.toggle_grayscale
        elif k == ord('g'):
            ip.toggle_grayscale = not ip.toggle_grayscale
        elif k == ord('f'):
            ip.toggle_face_detection = not ip.toggle_face_detection
        elif k == ord('z'):
            ip.threshold_delta -= 20
            print(ip.threshold_delta)
        elif k == ord('u'):
            ip.threshold_delta += 20
            print(ip.threshold_delta)

run(
    Camera('/dev/video1'),
    Camera('/dev/video3')
)

# import os

# run(
#     Camera(os.environ['V1']),
#     Camera(os.environ['V2'])
# )
