from dotenv import load_dotenv
import requests
import os
import json

from slack import WebClient

load_dotenv()

slack_oauth_token = os.environ['SLACK_OAUTH_TOKEN']
slack_user_token = os.environ['SLACK_USER_TOKEN']
# user_id = os.environ['USER_ID']

class SlackDriver:
    def __init__(self):
        self._headers = {'Content-Type': 'application/json'}

    def send_message(self, message, channel):
        params = {"token": slack_user_token,
                  "channel": channel, "text": message}

        r = requests.post('https://slack.com/api/chat.postMessage',
                          headers=self._headers, params=params)

        # print(r.text)

    def change_status_message(self, text, emoji):
        params = {
            "token": slack_oauth_token,
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

    def change_status(self, status):
        params = {
            "token": slack_oauth_token,
            "presence": status
        }
        # print(params)

        r = requests.post(
            'https://slack.com/api/users.setPresence', params=params)
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
            'token': slack_user_token,
            'channel': 'C01CRGA8QK0',
            'username': 'me',
            'blocks': json.dumps(blocks)
            # 'attachments': json.dumps(attachments)
        }

        r = requests.post(
            'https://slack.com/api/chat.postMessage', params=data)
        print(r.text)

    def read_presence(self, user):
        params = {"token": slack_user_token, "user":user}
        r = requests.post('https://slack.com/api/users.getPresence',
                          headers=self._headers, params=params)
        # print(r.text)
        return r.json()

    def users_list(self):
        params = {"token": slack_user_token}
        r = requests.post('	https://slack.com/api/users.list',
                          headers=self._headers, params=params)

        rjson = r.json()

        id_list = []
        name_list = []
        for i in range(0, len(rjson["members"])):
            id_list.append(rjson["members"][i]["id"])
            name_list.append(rjson["members"][i]["profile"]["display_name"])
        return id_list, name_list

    def delete_message(self, channel, time_stamp):
        params = {
            "token": slack_oauth_token,
            # "user": user_id,
            "channel": channel,
            "ts": time_stamp
        }
        # print(params)

        r = requests.post(
            'https://slack.com/api/users.profile.set', params=params)

    def conversation_history(self, channel):
        params = {
            "token": slack_oauth_token,
            # "user": user_id,
            "channel": channel,
            "limit": 5
        }
        print(params)

        r = requests.post(
            'https://slack.com/api/conversations.history', params=params)
        print(r.json())

    def conversation_list(self):
        params = {
            "token": slack_oauth_token,
        }
        print(params)

        r = requests.post(
            'https://slack.com/api/conversations.list', params=params)
        print(r.json())