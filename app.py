from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.exceptions import InvalidSignatureError
from openpyxl import Workbook, load_workbook
import os
import datetime

app = Flask(__name__)

# =========================
# LINE設定
# =========================
CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ab06793a22d874528049156bf4de7dc8"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ★管理者ID（ここ重要）
ADMIN_USER_ID = "U6b88cd42924581ac141db052cc09eb08"

# =========================
# データ管理
# =========================
REGIONS = ["福岡", "熊本", "大分", "佐賀", "長崎"]
USER_REGION = {}
FILE_NAME = "health_log.xlsx"

# =========================
# Excel保存
# =========================
def save_log(user_id, region, message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(FILE_NAME):
        wb = Workbook()
        ws = wb.active
        ws.append(["日時", "ユーザーID", "地域", "内容"])
        wb.save(FILE_NAME)

    wb = load_workbook(FILE_NAME)
    ws = wb.active
    ws.append([now, user_id, region, message])
    wb.save(FILE_NAME)

# =========================
# アラート送信
# =========================
def send_alert(user_id, region, message):
    alert_text = f"🚨【体調不良アラート】\nユーザー: {user_id}\n地域: {region}\n内容: {message}"
    line_bot_api.push_message(
        ADMIN_USER_ID,
        TextSendMessage(text=alert_text)
    )

# =========================
# ルート
# =========================
@app.route("/")
def index():
    return "健康チェックBOT起動中"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# =========================
# メイン処理
# =========================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    region = USER_REGION.get(user_id, "未登録")

    # ★Excel保存
    save_log(user_id, region, text)

    # =========================
    # 開始
    # =========================
    if text == "開始":
        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=r, text=r)) for r in REGIONS
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="まず地域を選択してください", quick_reply=buttons)
        )
        return

    # =========================
    # 地域選択
    # =========================
    if text in REGIONS:
        USER_REGION[user_id] = text

        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="元気です", text="元気です")),
            QuickReplyButton(action=MessageAction(label="少し元気です", text="少し元気です")),
            QuickReplyButton(action=MessageAction(label="かなり悪いです", text="かなり悪いです")),
        ])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"{text}で登録しました。\n\n🌟 元気ですか？ 🌟",
                quick_reply=buttons
            )
        )
        return

    # =========================
    # 元気
    # =========================
    if text == "元気です":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="よかったです！今日も一日頑張りましょう")
        )
        return

    # =========================
    # 少し元気
    # =========================
    if text == "少し元気です":
        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="はい", text="少し元気_はい")),
            QuickReplyButton(action=MessageAction(label="いいえ", text="少し元気_いいえ")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="大丈夫ですか？", quick_reply=buttons)
        )
        return

    if text == "少し元気_はい":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理せず様子を見てください")
        )
        return

    if text == "少し元気_いいえ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理せず休んでください")
        )
        return

    # =========================
    # かなり悪い（アラート）
    # =========================
    if text == "かなり悪いです":
        send_alert(user_id, region, text)

        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="体調", text="体調")),
            QuickReplyButton(action=MessageAction(label="メンタル", text="メンタル")),
        ])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="原因は何ですか？", quick_reply=buttons)
        )
        return

    # =========================
    # 体調
    # =========================
    if text == "体調":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理せずに病院に行かれてください")
        )
        return

    # =========================
    # メンタル
    # =========================
    if text == "メンタル":
        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="はい", text="メンタル_はい")),
            QuickReplyButton(action=MessageAction(label="いいえ", text="メンタル_いいえ")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="大丈夫ですか？", quick_reply=buttons)
        )
        return

    if text == "メンタル_はい":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理せず様子を見てください")
        )
        return

    # =========================
    # メンタル悪化（アラート）
    # =========================
    if text == "メンタル_いいえ":
        send_alert(user_id, region, text)

        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="個人", text="個人")),
            QuickReplyButton(action=MessageAction(label="仕事", text="仕事")),
        ])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="原因はどちらですか？", quick_reply=buttons)
        )
        return

    # =========================
    # 最終分岐
    # =========================
    if text == "個人":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="一人で悩まず誰かに相談してください")
        )
        return

    if text == "仕事":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="委員長が相談に乗ります。まず電話してください")
        )
        return