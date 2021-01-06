#-*- coding: utf-8 -*-
import numpy as np
import cv2
import face_recognition


def fface(img, draw_found=False):
    floc = face_recognition.face_locations(img, model='hog')
    if draw_found and len(floc) > 0:
        for f in floc:
            draw_rect(img, f)
    return floc


def flandmarks(img, faces=[], draw_found=False):
    fl = face_recognition.face_landmarks(img, face_locations=faces, model='large')[0]
    if fl and draw_found:
        for part in fl:
            for x, y  in fl[part]:
                cv2.rectangle(img, (x, y), (x+2, y+2), (255,0,0), 2)
    return fl


def draw_rect(img, rect):
    t,r,b,l = rect
    cv2.rectangle(img, (l, t), (r, b), (0,0,255), 2)


def threshold(gray, bal=None):
    if bal is None:
        bal = np.mean(gray)
    low_m = gray < bal
    high_m = gray > bal
    ret = np.copy(gray)
    ret[low_m] = 0
    ret[high_m] = 255
    return ret

def grayscale(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

def bgr2hsv(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

def rgb2hsv(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

def resize(iar, dims=()):
    return cv2.resize(iar, dims)
