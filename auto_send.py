from linebot import LineBotApi
from linebot.models import TextSendMessage
import datetime
import time

# =====================
# LINE設定（app.pyと同じもの）
# =====================
CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
USER_ID = "U6b88cd42924581ac141db052cc09eb08"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# =====================
# 時間設定（ここだけ変更）
# =====================
SEND_HOUR = 14
SEND_MINUTE = 42

# =====================
# 送信処理
# =====================
def send_message():
    try:
        message = "テスト送信"
        line_bot_api.push_message(USER_ID, TextSendMessage(text=message))
        print("送信成功")

    except Exception as e:
        print("＝＝＝＝エラー発生＝＝＝＝")
        print(e)
        print("＝＝＝＝ここまで＝＝＝＝")
# =====================
# スケジューラ
# =====================
print("自動送信スタート")

print("自動送信スタート")

send_message()  # ←これ追加（即送信テスト）


last_sent = None

print("自動送信スタート")

while True:
    now = datetime.datetime.now()

    # ★現在時刻表示（必須）
    print(f"現在: {now.strftime('%H:%M:%S')} / 設定: {SEND_HOUR}:{SEND_MINUTE}")

    if now.hour == SEND_HOUR and now.minute >= SEND_MINUTE:
        print("時間条件OK")

        if last_sent != now.strftime("%Y-%m-%d"):
            print("送信実行！")
            send_message()
            last_sent = now.strftime("%Y-%m-%d")

    time.sleep(5)