from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 1. 在此填入你在 LINE Developers 後台建立的 "Channel Access Token" 與 "Channel Secret"
line_bot_api = LineBotApi('edscbrUa3+bnwcgMJoTHavGF39/o/V2Llk2nztyNEH+XP1Sjg2J6QwofVQw7hnywumkGvdS/oPmUGgGb0Z2eI2NfB+0vhmWN4nYow/ycVuW/4p2JJSucBZtkgv9DvDONfm0j/2OexZMogXY0rpoiDAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4200b9e806175214a84a542f5a03e5d9')

# 2. LINE 推送消息的接收端 (webhook url)
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 HTTP 標頭中的 x-line-signature
    signature = request.headers['X-Line-Signature']
    # 取得 POST 請求中的內容
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 驗證不通過則回傳 400
        abort(400)

    return 'OK'


# 3. 當接收到文字訊息時，原封不動地回傳給使用者
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得使用者傳來的文字
    user_text = event.message.text
    # 直接回傳相同的文字
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=user_text)
    )

if __name__ == "__main__":
    app.run(debug=True, port=8000)