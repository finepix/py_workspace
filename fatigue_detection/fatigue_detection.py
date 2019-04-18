#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2019/4/3 16:57
# @Author  : shawn_zhu
# @Site    : 
# @File    : fatigue_detection.py
# @Software: PyCharm

'''

import cv2

eye_cascade_source = 'resources/haarcascade_eye.xml'

def test_detection_for_eyes():
    eye_cascade = cv2.CascadeClassifier(eye_cascade_source)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        # gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # eyes = eye_cascade.detectMultiScale(gray_img, scaleFactor=1.15, minSize=(5, 5))

        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

if __name__ == '__main__':
    test_detection_for_eyes()
