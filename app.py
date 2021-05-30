#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('8OtKwi3rjxZL7PA6YXJkGTrSqzvt6Rfju1TGM4Se0t9wO8eTMUizJbIX0DEFk8MOvjw/iIPvHy6LyQO5XZP34RgH9MF4Yh+ZothnbvUXghZm//R4PT9RthLA/KssqSjQBNaffBT3Zrc86RE+CFSyzQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('f930a45b3290b4c3a35daa9e55fd760e')

line_bot_api.push_message('U0f84a7f70cfdf86b7afa00cd651f5836', TextSendMessage(text='漲翻天！'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
