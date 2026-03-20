from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from linebot.exceptions import InvalidSignatureError

import os
import datetime
from openpyxl import Workbook, load_workbook

app = Flask(__name__)

<<<<<<< HEAD
# =====================
# LINE設定
# =====================
CHANNEL_ACCESS_TOKEN = "ここにアクセストークン"
CHANNEL_SECRET = "ここにシークレット"
=======
# =========================
# LINE設定
# =========================
CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ab06793a22d874528049156bf4de7dc8"
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

<<<<<<< HEAD
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
=======
# =========================
# ユーザー管理
# =========================
USER_IDS = ["U6b88cd42924581ac141db052cc09eb08",]
USER_STATE = {}

# =========================
# ログ（安全版）
# =========================
def save_log(user_id, message):
    print(user_id, message)

# =========================
# ルート確認
# =========================
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)
@app.route("/")
def index():
    return "生存確認BOT起動中"

<<<<<<< HEAD
# =====================
# Webhook
# =====================
@app.route("/callback", methods=['POST'])
=======
# =========================
# LINE受信
# =========================
@app.route("/callback", methods=["POST"])
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

<<<<<<< HEAD
# =====================
# テキスト処理
# =====================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
=======
# =========================
# メッセージ処理
# =========================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)
    text = event.message.text
    user_id = event.source.user_id

<<<<<<< HEAD
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
=======
    if user_id not in USER_IDS:
        USER_IDS.append(user_id)

    state = USER_STATE.get(user_id, "normal")

    print("状態:", state, "入力:", text)

    # =========================
    # 元気ですか？
    # =========================
    if text == "はい" and state == "normal":
        USER_STATE[user_id] = "normal"
        save_log(user_id, "元気：はい")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="その調子で頑張りましょう")
        )

    elif text == "いいえ" and state == "normal":
        USER_STATE[user_id] = "confirm_condition"
        save_log(user_id, "元気：いいえ")
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
<<<<<<< HEAD
                text="位置情報の送信方法：\n①下のボタンを押す\n②位置情報を許可\n③そのまま送信してください",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=LocationAction(label="位置情報を送る")
                        )
=======
                text="大丈夫ですか？",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="はい", text="はい")),
                        QuickReplyButton(action=MessageAction(label="いいえ", text="いいえ")),
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)
                    ]
                )
            )
        )

<<<<<<< HEAD
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
=======
    # =========================
    # 大丈夫ですか？
    # =========================
    elif text == "はい" and state == "confirm_condition":
        USER_STATE[user_id] = "normal"
        save_log(user_id, "体調：はい")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理せずに休んでください")
        )

    elif text == "いいえ" and state == "confirm_condition":
        USER_STATE[user_id] = "waiting_location"
        save_log(user_id, "体調：いいえ（要対応）")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="電話しましょうか？\n位置情報を送ってください",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=LocationAction(label="位置情報を送る"))
                    ]
                )
            )
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ボタンで選択してください")
        )

# =========================
# GPS受信
# =========================
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    user_id = event.source.user_id
    lat = event.message.latitude
    lon = event.message.longitude

<<<<<<< HEAD
    save_log(user_id, f"位置情報: {lat},{lon}")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="位置情報を受け取りました。ありがとうございます。")
    )
=======
    USER_STATE[user_id] = "normal"
    save_log(user_id, f"GPS: {lat}, {lon}")

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="位置情報ありがとうございます")
    )

# =========================
# 全員送信（ボタン付き）
# =========================
@app.route("/send")
def send_all():
    for user_id in USER_IDS:
        line_bot_api.push_message(
            user_id,
            TextSendMessage(
                text="元気ですか？",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="はい", text="はい")),
                        QuickReplyButton(action=MessageAction(label="いいえ", text="いいえ")),
                    ]
                )
            )
        )
        save_log(user_id, "元気ですか送信")

    return "送信完了"

# =========================
# 起動
# =========================
if __name__ == "__main__":
    app.run()
>>>>>>> fabb045 (生存確認BOT完成（ボタン操作・体調確認・GPS対応）)
