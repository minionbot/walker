# coding: utf-8
# Copyright © 2018 All Rights Reserved.
# Wangjing (wangjild@gmail.com)

from django.conf import settings

from slackclient import SlackClient
from octopus.celery import app

@app.task(name = 'octopus.tasks.send_slack')
def send_slack(channel, name, image_url, reference):
    slack_token = settings.SLACK_API_TOKEN
    sc = SlackClient(slack_token)

    results = sc.api_call(
      "chat.postMessage",
      channel=channel,
      attachments = [
        {
            "fallback": name,
            "color": "#36a64f",
            # "author_name": "Bobby Tables",
            # "author_link": "http://flickr.com/bobby/",
            # "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": name,
            "title_link": reference,
            # "text": "Optional text that appears within the attachment",
            "image_url": image_url,
            "thumb_url": image_url,
        }
      ])

    return results


