import cv2

class Viewer(object):
    def __init__(self, *cameras):
        for n, cam in enumerate(cameras):
            cv2.namedWindow(str(n), cv2.WINDOW_GUI_NORMAL)
            cv2.setWindowTitle(str(n), cam.device)

    def update_all(self, *frames):
        for n, frame in frames:
            cv2.imshow(str(n), frame)
        
    def update_cam(self, cam_id, frame):
        cv2.imshow(str(cam_id), frame)

    def close(self):
        cv2.destroyAllWindows()
