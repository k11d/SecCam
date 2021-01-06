from .image_utils import fface, threshold, grayscale


class ImageProcessing(object):

    toggle_face_detection = False
    toggle_grayscale = False
    toggle_threshold = False
    threshold_delta = 5
    threshold_limit = 100

    def apply_all(self, frame):
        frame = grayscale(frame) if self.toggle_grayscale else frame
        frame = threshold(frame, self.threshold_delta) if self.toggle_threshold else frame
        if self.toggle_face_detection:
            fface(frame, draw_found=True)
        return frame


