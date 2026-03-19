from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, MessageAction,
    LocationMessage
)
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "ab06793a22d874528049156bf4de7dc8"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def index():
    return "生存確認BOT（最終完成版）"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# 🔥 テキスト処理
@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):

    text = event.message.text

    # ▼はい
    if text == "はい":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="安心しました😊")
        )

    # ▼いいえ（完全誘導版）
    elif text == "いいえ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=(
                    "⚠️大丈夫ですか？\n\n"
                    "📍現在地を送ってください\n\n"
                    "【送り方】\n"
                    "① 文字入力を閉じる（キーボードを消す）\n"
                    "② 左下の『＋』ボタンを押す\n"
                    "③『位置情報』を選ぶ\n"
                    "④ そのまま送信ボタンを押す\n\n"
                    "※わからなければ『わからない』と送ってください"
                )
            )
        )

    # ▼位置説明（さらに丁寧）
    elif text == "位置":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=(
                    "📍【位置情報の送り方】\n\n"
                    "① 文字入力を閉じる（キーボードを消す）\n"
                    "② 左下の『＋』を押す\n"
                    "③『位置情報』を押す\n"
                    "④ 地図が出たら送信ボタンを押す\n\n"
                    "これで現在地が送れます"
                )
            )
        )

    # ▼サポート
    elif text == "わからない":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=(
                    "📱画面の左下に『＋』があります\n"
                    "キーボードを消すと見えるようになります"
                )
            )
        )

    # ▼その他（ボタン表示）
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="生存確認",
                template=ButtonsTemplate(
                    text="元気ですか？",
                    actions=[
                        MessageAction(label="はい", text="はい"),
                        MessageAction(label="いいえ", text="いいえ"),
                        MessageAction(label="📍位置の送り方", text="位置")
                    ]
                )
            )
        )


# 🔥 GPS処理（地図リンク付き）
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):

    lat = event.message.latitude
    lon = event.message.longitude

    map_url = f"https://www.google.com/maps?q={lat},{lon}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=(
                "📍位置を受信しました\n"
                f"{map_url}"
            )
        )
    )


if __name__ == "__main__":
    app.run()