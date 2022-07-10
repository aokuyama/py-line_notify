from os import getenv
from linebot import LineBotApi
from linebot.models import TextSendMessage
from line_notify.notice import Notice


class LineBot:
    _api: LineBotApi

    def __init__(self, access_token: str = None) -> None:
        if not access_token:
            access_token = getenv('LINE_CHANNEL_ACCESS_TOKEN')
        self._api = LineBotApi(access_token)

    def send(self, notice: Notice):
        msg = {
            "text": notice.getMsg()
        }
        emojis = notice.getEmojis()
        if len(emojis):
            msg['emojis'] = emojis

        tsm = TextSendMessage(**msg)
        if notice.isReply():
            self._api.reply_message(notice.getReplyToken(), TextSendMessage(text='Hello World!'))
        if notice.isBroadcast():
            self._api.broadcast(tsm)
        else:
            self._api.push_message(notice.getTo(), tsm)
