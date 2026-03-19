from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from linebot.exceptions import InvalidSignatureError

import os
import datetime
from openpyxl import Workbook, load_workbook

app = Flask(__name__)

# =====================
# LINE設定
# =====================
CHANNEL_ACCESS_TOKEN = "ここにアクセストークン"
CHANNEL_SECRET = "ここにシークレット"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# =====================
# ログ保存
# =====================
def save_log(user_id, action):
    file_name = "action_log.xlsx"

    if not os.path.exists(file_name):
        wb = Workbook()
        ws = wb.active
        ws.append(["日時", "ユーザーID", "内容"])
        wb.save(file_name)

    wb = load_workbook(file_name)
    ws = wb.active

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([now, user_id, action])

    wb.save(file_name)

# =====================
# 起動確認
# =====================
@app.route("/")
def index():
    return "生存確認BOT起動中"

# =====================
# Webhook
# =====================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# =====================
# テキスト処理
# =====================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id

    # 全ログ
    save_log(user_id, f"受信: {text}")

    # =====================
    # はい
    # =====================
    if text == "はい":
        save_log(user_id, "元気（はい）")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="安心しました。無理せず頑張ってください")
        )

    # =====================
    # いいえ
    # =====================
    elif text == "いいえ":
        save_log(user_id, "いいえ選択")

        message = TemplateSendMessage(
            alt_text="位置情報確認",
            template=ButtonsTemplate(
                text="よかったら位置情報を教えてください",
                actions=[
                    MessageAction(label="送る", text="位置送信"),
                    MessageAction(label="送らない", text="送らない")
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, message)

    # =====================
    # 送る
    # =====================
    elif text == "位置送信":
        save_log(user_id, "位置送信選択")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="位置情報の送信方法：\n①下のボタンを押す\n②位置情報を許可\n③そのまま送信してください",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=LocationAction(label="位置情報を送る")
                        )
                    ]
                )
            )
        )

    # =====================
    # 送らない
    # =====================
    elif text == "送らない":
        save_log(user_id, "送信拒否")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理をせずに休んでください")
        )

    # =====================
    # その他
    # =====================
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="メッセージを受け取りました")
        )

# =====================
# 位置情報処理
# =====================
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    user_id = event.source.user_id
    lat = event.message.latitude
    lon = event.message.longitude

    save_log(user_id, f"位置情報: {lat},{lon}")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="位置情報を受け取りました。ありがとうございます。")
    )