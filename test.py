import cv2
from datetime import datetime
import dlib
from imutils import face_utils

import subprocess
import os
from dotenv import load_dotenv

import requests
from datetime import date
import json

from slack import WebClient

load_dotenv()

# client = WebClient(token=os.environ['SLACK_OAUTH_TOKEN'])
slack_oauth_token = os.environ['SLACK_OAUTH_TOKEN']
user_id = os.environ['USER_ID']


class SlackDriver:

    def __init__(self, _token):
        self._token = _token
        self._headers = {'Content-Type': 'application/json'}

    def change_status(self, text, emoji):
        data = {
            "token": os.environ['SLACK_OAUTH_TOKEN'],
            # "user": user_id,
            "profile": json.dumps({
                "status_text": text,
                "status_emoji": emoji
            })
        }
        print(data)

        r = requests.post(
            'https://slack.com/api/users.profile.set', params=data)
        print(r.text)


if __name__ == '__main__':
    token = slack_oauth_token
    slack = SlackDriver(token)
    slack.change_status("hello from 'test.py'", ':smile:')
