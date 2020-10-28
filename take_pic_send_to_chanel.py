# cd Documents/Waseda3rdYear/ProjectResearchB/slack_api
# python3 test.py

import cv2
from datetime import datetime
import dlib
from imutils import face_utils

import subprocess
import os
from dotenv import load_dotenv
# from slackclient import SlackClient
import requests
from datetime import date

from slack import WebClient

load_dotenv()

# slack_token = os.environ['SLACK_TOKEN']
# client = SlackClient(slack_token)
client = WebClient(token=os.environ['SLACK_TOKEN'])

face_detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)


class SlackDriver:

    def __init__(self, _token):
        self._token = _token  # api_token
        self._headers = {'Content-Type': 'application/json'}

    def send_message(self, message, channel):
        params = {"token": self._token, "channel": channel, "text": message}

        r = requests.post('https://slack.com/api/chat.postMessage',
                          headers=self._headers,
                          params=params)

        # print("return ", r.json())


def cpture_save():
    cap = cv2.VideoCapture(0)
    n = 0
    no_face_for = 0
    hello_for = 0
    while True:
        # get 1frame
        ret, frame = cap.read()
        # if no frame then close
        if (not ret):
            break
        if (n < 10):
            n += 1
            continue

        dets = face_detector(frame, 1)
        det_str = str(dets)
        print(str(dets))
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(date)
        if (det_str == 'rectangles[]'):
            no_face_for += 1
            if no_face_for == 10:
                hello_for = 0
                print('no face')
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                slack.send_message(
                    "You are offline... [" + date + "]", "#imactive-response")
        else:
            hello_for += 1
            if hello_for == 10:
                no_face_for = 0
                slack.send_message(
                    "Hello, you are here! [" + date + "]", "#imactive-response")

        # show window
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        # EscKey closes the program
        if key == 27:
            break
        n += 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    token = os.environ['SLACK_TOKEN']  # TODO your token.
    slack = SlackDriver(token)

    cpture_save()
