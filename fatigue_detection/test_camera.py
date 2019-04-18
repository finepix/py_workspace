#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2019/4/3 16:48
# @Author  : shawn_zhu
# @Site    : 
# @File    : test_camera.py
# @Software: PyCharm

'''


import cv2


def run():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frome = cap.read()

        cv2.imshow('camera', frome)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

if __name__ == '__main__':
    run()