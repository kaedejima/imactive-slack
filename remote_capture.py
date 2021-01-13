# RUN FROM TERMINAL
# cd Documents/Waseda3rdYear/ProjectResearchB/slack_api
# python3 remote_capture.py

import cv2
from datetime import datetime
import dlib
from imutils import face_utils
import imutils

# import subprocess
import os
from dotenv import load_dotenv
import requests
# from datetime import date
import json
import time
import datetime
import pandas as pd
import numpy as np

import slack_funcs
SF = slack_funcs.SlackDriver()

face_detector = dlib.get_frontal_face_detector()
predictor_path = './source/shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)

away_emoji = ':sweat_drops:'
active_emoji = ':thumbsup:'

def capture():
    cap = cv2.VideoCapture(0)
    # cap.set(4, 320)
    n = 0
    no_face_for = 0
    hello_for = 0
    while True:
        # get 1frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=320)
        # if no frame then close
        if (not ret):
            print('ERROR: NOT RET')
            break
        if (n < 10):
            n += 1
            continue

        dets = face_detector(frame, 1)
        det_str = str(dets)
        # print(str(dets))
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(date)
        if (det_str == 'rectangles[]'):
            no_face_for += 1
            if no_face_for == 30:
                hello_for = 0
                print('no face')
                detected_inactive(date)
        else:
            hello_for += 1
            if hello_for == 30:
                no_face_for = 0
                print('hello face')
                detected_active(date)

        # show window
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        # EscKey closes the program
        if key == 27:
            print('EXIT: KEY == 27')
            break
        n += 1

    cap.release()
    SF.change_status_message('', '')
    cv2.destroyAllWindows()


def detected_inactive(date):
    # SF.send_message("You are offline... [" + date + "]", "#imactive-response")
    SF.change_status('away')
    SF.change_status_message("I'm away...", away_emoji)



def detected_active(date):
    # SF.send_message("Hello, you are here! [" + date + "]", "#imactive-response")
    SF.change_status('auto')
    SF.change_status_message("Hi, I'm available!", active_emoji)


capture()