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
slack_user_token = os.environ['SLACK_USER_TOKEN']
user_id = os.environ['USER_ID']


class SlackDriver:

    def __init__(self, _token):
        self._token = _token
        self._headers = {'Content-Type': 'application/json'}

    def send_option(self):
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

        data = {
            'token': token,
            'channel': 'C01CRGA8QK0',
            'username': 'me',
            'attachments': json.dumps(attachments)
        }

        r = requests.post(
            'https://slack.com/api/chat.postMessage', params=data)
        print(r.text)


if __name__ == '__main__':
    token = slack_user_token
    slack = SlackDriver(token)
    slack.send_option()
