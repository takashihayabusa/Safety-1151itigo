from linebot import LineBotApi
from linebot.models import TextSendMessage
import datetime
import time

# =====================
# LINE設定
# =====================
CHANNEL_ACCESS_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
USER_ID = "U6b88cd42924581ac141db052cc09eb08"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# =====================
# ★ここに追加（重要）
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
# 時間設定
# =====================
SEND_HOUR = 16
SEND_MINUTE = 6

# =====================
# 送信関数（★先に書く）
# =====================
def send_message():
    try:
        message = "【自動送信】元気ですか？"
        line_bot_api.push_message(USER_ID, TextSendMessage(text=message))
        save_log(USER_ID, "元気ですか送信")
        print("送信成功")
    except Exception as e:
        print("エラー:", e)

# =====================
# メイン処理（後）
# =====================
print("自動送信スタート")



while True:
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

    print(f"今の時間: {now.strftime('%H:%M:%S')}")

    if now.hour == SEND_HOUR and now.minute == SEND_MINUTE:
        print("時間一致！！！")
        send_message()
        time.sleep(60)

    time.sleep(5)