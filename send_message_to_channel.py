import subprocess
import os
from dotenv import load_dotenv
from slackclient import SlackClient
import requests
from datetime import date


load_dotenv()

slack_token = os.environ['SLACK_TOKEN']
client = SlackClient(slack_token)


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


if __name__ == '__main__':
    token = os.environ['SLACK_TOKEN']  # TODO your token.
    slack = SlackDriver(token)
    today = date.today()
    slack.send_message("Hello World! from python" +
                       str(today), "#imactive-response")
