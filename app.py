from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# ★自分の情報
CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ab06793a22d874528049156bf4de7dc8"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def index():
    return "生存確認BOT 起動中"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print("エラー:", e)
        abort(500)

    return "OK"


# ★メッセージ受信（ここが元の安定動作）
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_text = event.message.text

    # ▼「はい」
    if user_text == "はい":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="安心しました😊")
        )

    # ▼「いいえ」
    elif user_text == "いいえ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="大丈夫ですか？連絡してください⚠️")
        )

    # ▼それ以外
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="生存確認",
                template=ButtonsTemplate(
                    text="元気ですか？",
                    actions=[
                        MessageAction(label="はい", text="はい"),
                        MessageAction(label="いいえ", text="いいえ")
                    ]
                )
            )
        )