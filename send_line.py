from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_TOKEN = "G+WVfBYA61JkTqXM+r1/Y3HlksAxH2sq8lm/Zm2ifIr6agVcr339zAbjUfmZSp5tkyB97l0pG681K7hGtUnbmXnV2CyG8O7t/dTDhoA9CJI94aftXczCEfFwmWTTEu3tdLWNDWiHH7lzrW4uPX0UOgdB04t89/1O/w1cDnyilFU="
GROUP_ID = "U6b88cd42924581ac141db052cc09eb08"

line_bot_api = LineBotApi(LINE_TOKEN)

url = "https://safty-itigo1151.pythonanywhere.com"

message = f"""
おはようございます

健康チェックをお願いします

{url}
"""

line_bot_api.push_message(GROUP_ID, TextSendMessage(text=message))