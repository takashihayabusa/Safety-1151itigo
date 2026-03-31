def handle_emergency(line_bot_api, event, user_id, text, USER_STATE):

    # ===== 緊急開始 =====
    if text == "緊急開始":
        USER_STATE[user_id] = "emergency_status"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="現在の状況を教えてください",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="安全", text="安全")),
                        QuickReplyButton(action=MessageAction(label="ケガあり", text="ケガあり")),
                        QuickReplyButton(action=MessageAction(label="危険", text="危険"))
                    ]
                )
            )
        )
        return True

    # ===== 状況 =====
    if USER_STATE.get(user_id) == "emergency_status":

        if text == "安全":
            USER_STATE[user_id] = "end"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無事でよかったです🙏")
            )
            return True

        if text == "ケガあり":
            USER_STATE[user_id] = "end"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="ケガをされているのですね。\n救急車を呼べますか？周りの人に助けを求めてください🙏"
                )
            )
            return True

        if text == "危険":
            USER_STATE[user_id] = "end"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text="危険な状況です。\n安全な場所に避難してください。周りの人と一緒に行動してください🙏"
                )
            )
            return True

    return False