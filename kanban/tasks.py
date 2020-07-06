from __future__ import absolute_import, unicode_literals

from celery import shared_task
import slack


@shared_task
def send_slack_message(slack_bot_token, slack_channel_id, mensaje):
    client = slack.WebClient(token=slack_bot_token)
    client.chat_postMessage(
        channel=slack_channel_id,
        text=mensaje
    )
    print("Ejecutado en celery")