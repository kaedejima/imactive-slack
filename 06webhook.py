# RUN FROM TERMINAL
# cd Documents/Waseda3rdYear/ProjectResearchB/slack_api
# python3 06webhook.py

import slackweb
# import os
# from dotenv import load_dotenv
# load_dotenv()


slack = slackweb.Slack(
    url="https://hooks.slack.com/services/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")
# print(os.environ['WEBHOOK_URL'])
slack.notify(text="Hello from webhook.py")
