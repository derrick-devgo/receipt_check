from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 1. 在此填入你在 LINE Developers 後台建立的 "Channel Access Token" 與 "Channel Secret"
line_bot_api = LineBotApi('edscbrUa3+bnwcgMJoTHavGF39/o/V2Llk2nztyNEH+XP1Sjg2J6QwofVQw7hnywumkGvdS/oPmUGgGb0Z2eI2NfB+0vhmWN4nYow/ycVuW/4p2JJSucBZtkgv9DvDONfm0j/2OexZMogXY0rpoiDAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4200b9e806175214a84a542f5a03e5d9')

def check_invoice(num: str) -> str:
    """回傳中獎結果的文字，如果沒中獎，則回傳空字串。"""
    
    # 特別獎、特獎、頭獎號碼（可自行修改）
    ns = '28630525'                           # 特別獎 1000 萬
    n1 = '90028580'                           # 特獎   200 萬
    n2 = ['27435934', '39666605', '02550031'] # 頭獎   20 萬（含末 3~7 碼各級獎）
    
    # 先檢查特別獎 (1000 萬)
    if num == ns:
        return '對中 1000 萬元！'
    
    # 再檢查特獎 (200 萬)
    if num == n1:
        return '對中 200 萬元！'
    
    # 頭獎與其對應末 3~7 碼的各級獎
    for i in n2:
        if num == i:
            return '對中 20 萬元！'
        elif num[-7:] == i[-7:]:
            return '對中 4 萬元！'
        elif num[-6:] == i[-6:]:
            return '對中 1 萬元！'
        elif num[-5:] == i[-5:]:
            return '對中 4000 元！'
        elif num[-4:] == i[-4:]:
            return '對中 1000 元！'
        elif num[-3:] == i[-3:]:
            return '對中 200 元！'
    
    # 都沒中
    return '很可惜，沒有中獎。'

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
    user_text = event.message.text.strip()

    # 判斷是否為 8 碼數字，如果是，嘗試對獎
    if len(user_text) == 8 and user_text.isdigit():
        result = check_invoice(user_text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    else:
        # 否則進行「鸚鵡回覆」
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="不好意思，請輸入八位數統一發票號碼")
        )

if __name__ == "__main__":
    app.run(debug=True, port=8000)