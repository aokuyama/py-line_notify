import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
group_id = os.getenv('LINE_GROUP_ID')
msg = 'Hello World!'

line_bot_api = LineBotApi(channel_access_token)
line_bot_api.push_message(group_id, TextSendMessage(text=msg))
