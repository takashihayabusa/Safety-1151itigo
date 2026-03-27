from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE設定
CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ab06793a22d874528049156bf4de7dc8"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 地域リスト
REGIONS = ["福岡", "熊本", "大分", "佐賀", "長崎"]

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    # =========================
    # 開始 → 地域選択
    # =========================
    if text == "開始":
        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label=r, text=r)) for r in REGIONS
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="まず地域を選択してください",
                quick_reply=buttons
            )
        )
        return

    # =========================
    # 地域選択 → 健康チェック
    # =========================
    if text in REGIONS:
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
            TextSendMessage(
                text="大丈夫ですか？",
                quick_reply=buttons
            )
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
    # かなり悪い
    # =========================
    if text == "かなり悪いです":
        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="体調", text="体調")),
            QuickReplyButton(action=MessageAction(label="メンタル", text="メンタル")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="原因は何ですか？",
                quick_reply=buttons
            )
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
            TextSendMessage(
                text="大丈夫ですか？",
                quick_reply=buttons
            )
        )
        return

    if text == "メンタル_はい":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無理せず様子を見てください")
        )
        return

    if text == "メンタル_いいえ":
        buttons = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="個人", text="個人")),
            QuickReplyButton(action=MessageAction(label="仕事", text="仕事")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="原因はどちらですか？",
                quick_reply=buttons
            )
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