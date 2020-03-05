import sys
import time
import datetime
import calendar
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
GDriveJSON = 'line-bot.json'
GSpreadSheet = 'UploadByline-bot'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
key = SAC.from_json_keyfile_name(GDriveJSON, scope)
gc = gspread.authorize(key)
worksheet = gc.open(GSpreadSheet).sheet1

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('RcNVpDxw1KT5fXiqOxO8IV0UDVMxyASjyRoytm5YIQs+n3rpKPDNc4EaB73hOPrkhUP4/WKZhEWVm2+xaIrHcYKe6ZI5sDaQj2C1koCXra7gB1CncwnVHJ8raeQ0ocP0LPkzons6q5ZDNix9w6xYiQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f41862ba4f038bff84debe318aa9ab54')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # user_id = event.source.user_id
    # line_bot_api.reply_message(event.reply_token, message)
    to = "Cf16b59adb11f8026dfb7ff7547af0959"
    toOusen = "C44fffd3a5d768c90caf8e6b3ca3c880d"
    if event.source.type == "group":
        group_id = event.source.group_id
        print("group_id =", group_id)
        if group_id == "C49598b4a99067a3989b7b0fb04eead6a":
            messagereplace = event.message.text
            messagereplace = messagereplace.replace('【IFTTT】 \n','')
            message = TextSendMessage(text=messagereplace)
            line_bot_api.push_message(toOusen, message)
    elif event.source.type == "user":
        user_id = event.source.user_id
        profile = line_bot_api.get_profile(event.source.user_id)
        displayName = profile.display_name
        Status_message = str(profile.status_message)
        # print("user_id =", user_id)
        # print("displayName =", displayName)
        # print("text =", event.message.text)
        # print(displayName + ": ", event.message.text)
        # if event.message.text == "咚":
        #     message = TextSendMessage(text="良")
        # elif event.message.text == "咔":
        #     message = TextSendMessage(text="良")
        # else:
        #     message = TextSendMessage(text="不可")
        today = (datetime.datetime.now()+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row((today, displayName, event.message.text))
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
