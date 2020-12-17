# RUN FROM TERMINAL
# cd Documents/Waseda3rdYear/ProjectResearchB/slack_api
# python3 10.py

import cv2
from datetime import datetime
import dlib
from imutils import face_utils
import imutils

import subprocess
import os
from dotenv import load_dotenv
import requests
from datetime import date
import json
import time
import pandas as pd
import numpy as np

from slack import WebClient

load_dotenv()

slack_oauth_token = os.environ['SLACK_OAUTH_TOKEN']
slack_user_token = os.environ['SLACK_USER_TOKEN']
user_id = os.environ['USER_ID']

face_detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)

class SlackDriver:
    def __init__(self, _oauth_token, _user_token):
        self._oauth_token = _oauth_token  # api_token
        self._user_token = _user_token
        self._headers = {'Content-Type': 'application/json'}

    def send_message(self, message, channel):
        params = {"token": self._user_token,
                  "channel": channel, "text": message}

        r = requests.post('https://slack.com/api/chat.postMessage',
                          headers=self._headers, params=params)

        # print(r.text)

    def change_status(self, text, emoji):
        params = {
            "token": self._oauth_token,
            # "user": user_id,
            "profile": json.dumps({
                "status_text": text,
                "status_emoji": emoji
            })
        }
        # print(params)

        r = requests.post(
            'https://slack.com/api/users.profile.set', params=params)
        # print(r.text)

    def send_button(self):
        callback_id = 'status_show_all'
        attachments = [{
            'text': 'Show status of ...',
            'callback_id': callback_id,
            'color': '#EE2222',
            'attachment_type': 'default',
            'actions': [{
                'name': 'all',
                'text': 'ALL',
                'type': 'button'
            },
                {
                'name': 'self',
                'text': 'YOU',
                'type': 'button'
            }]
        }]

        element_user_selector = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Which user do you want to check?"
            },
            "accessory": {
                "type": "users_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a user",
                },
                "action_id": "users_select-action"
            },
        }
        element_button = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Show All Status"
                    },
                    "value": "show_all",
                    "action_id": "button"
                }]
        }
        blocks = [element_button, element_user_selector]

        data = {
            'token': self._user_token,
            'channel': 'C01CRGA8QK0',
            'username': 'me',
            'blocks': json.dumps(blocks)
            # 'attachments': json.dumps(attachments)
        }

        r = requests.post(
            'https://slack.com/api/chat.postMessage', params=data)
        print(r.text)

    def read_presence(self, user):
        params = {"token": self._user_token, "user":user}
        r = requests.post('https://slack.com/api/users.getPresence',
                          headers=self._headers, params=params)
        # print(r.text)
        return r.json()

    def users_list(self):
        params = {"token": self._user_token}
        r = requests.post('	https://slack.com/api/users.list',
                          headers=self._headers, params=params)

        rjson = r.json()
        # print(rjson)
        # presence_str = ''
        member_list = []
        for i in range(0, len(rjson["members"])):  # range(0, #of menbers)
            # print(rjson["members"][i]["id"])
            member_list.append(rjson["members"][i]["id"])
        return member_list
        # #     presence = self.read_presence(rjson["members"][i]["id"])
        # #     presence_str += str(rjson["members"][i]["name"]) + ' is ' + str(presence["presence"]) + '\n'
        # # self.send_message(presence_str,'#imactive-response')
        # for member_id in member_list:
        #     res = self.read_presence(member_id)
        #     print(res)

    def track_presence(self, member_list):
        start_time = time.time()
        seconds = 4
        col = ['Time']+member_list
        df = pd.DataFrame(columns=col)
        print(col)
        tmp_flag = False

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time == seconds:
                start_time = time.time()
                res_list = [current_time]
                for member_id in member_list:
                    res_list.append(self.read_presence(member_id)['presence'])
                    # print(res_list)
                    # df.append(self.read_presence(member_id), ignore_index=True)
                # print(len(res_list), df.columns)
                df.loc[len(df)] = res_list
                print(res_list)
                # if (tmp_flag == False):
                #     tmp_flag = True
                #     print(df)
                # else:
                #     print(res_list)
                # print(df)

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
            break
        if (n < 10):
            n += 1
            continue

        dets = face_detector(frame, 1)
        det_str = str(dets)
        # print(str(dets))
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(date)
        if (det_str == 'rectangles[]'):
            no_face_for += 1
            if no_face_for == 10:
                hello_for = 0
                print('no face')
                detected_inactive(date)
        else:
            hello_for += 1
            if hello_for == 10:
                no_face_for = 0
                print('hello face')
                detected_active(date)

        # show window
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        # EscKey closes the program
        if key == 27:
            break
        n += 1

    cap.release()
    slack.change_status('', '')
    cv2.destroyAllWindows()


def detected_inactive(date):
    slack.send_message(
        "You are offline... [" + date + "]", "#imactive-response")
    slack.change_status('I am offline...', ':hear_no_evil:')


def detected_active(date):
    slack.send_message(
        "Hello, you are here! [" + date + "]", "#imactive-response")
    slack.change_status('Hi, I am available!', ':thumbsup:')

def create_object():
    pass

if __name__ == '__main__':
    slack = SlackDriver(slack_oauth_token, slack_user_token)
    # slack.send_button()
    member_list = slack.users_list()
    slack.track_presence(member_list)