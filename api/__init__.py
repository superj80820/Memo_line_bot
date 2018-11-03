
# coding: utf-8
#最後目的地要修改
#附近周遭站牌的檔案限制為10kb 必須要留意 目前已站牌只顯示25個為解決方法 但是因該要採用10kb來限制的方法 才合理
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,ImagemapSendMessage,BaseSize,URIImagemapAction,
    ImagemapArea,MessageImagemapAction,FollowEvent,LocationMessage,LocationSendMessage,CarouselTemplate,
    CarouselColumn,PostbackAction,URIAction,MessageAction,TemplateSendMessage, PostbackEvent
)
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from setting import *
line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)
app = Flask(__name__)
CORS(app)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print(body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    conn = sqlite.connect('%s/data/db/user_data.db'%(FileRoute))
    c = conn.cursor()
    c.execute("CREATE TABLE %s(Memo TEXT,status DEFAULT 'working')"%(event.source.user_id))
    conn.commit()
    conn.close()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='以創建備忘囉~喵\n請直接輸入要備忘的事情~'))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    def get_contents(memo):
        content = []
        for item in memo:
            content += [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "gravity": "center",
                        "text": item[0],
                        "flex": 3
                        },
                        {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "gravity": "center",
                        "action": {  
                            "type":"postback",
                            "label":"完成",
                            "data": item[0]
                        },
                        "flex": 1
                        }
                    ]
                }
            ]
        return content

    if event.message.text=='喵皇上 臣把事辦好拉!':
        conn = sqlite.connect('%s/data/db/user_data.db'%(FileRoute))
        c = conn.cursor()
        memo = c.execute("SELECT Memo FROM %s WHERE status ='working'"%(event.source.user_id))
        memo = memo.fetchall()
        conn.commit()
        conn.close()

        if memo != []:
            contents = get_contents(memo)
            flex={
                "type":"flex",
                "altText":"This is a Flex Message",
                "contents":{
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.imgur.com/cdSahMt.jpg",
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "哪尼!你又完成了哪一件!?",
                                "weight": "bold",
                                "size": "xl"
                                }
                            ]
                        },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": contents,
                        "flex": 0
                    }
                }
            }
            headers = {'Content-Type':'application/json','Authorization':'Bearer %s'%(LINE_TOKEN)}
            payload = {
                'replyToken':event.reply_token,
                'messages':[flex]
                }
            res=requests.post('https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(payload))
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='目前沒記事呀'))

    elif event.message.text == "喵皇上 臣完成了甚麼事?":
        conn = sqlite.connect('%s/data/db/user_data.db'%(FileRoute))
        c = conn.cursor()
        memo = c.execute("SELECT Memo FROM %s WHERE status ='done'"%(event.source.user_id))
        memo = memo.fetchall()
        conn.commit()
        conn.close()
        
        if memo != []:
            messages = ''
            for item in memo:
                messages += '%s\n'%(item[0])
            messages = messages[0:len(messages)-1]
                
            headers = {'Content-Type':'application/json','Authorization':'Bearer %s'%(LINE_TOKEN)}
            payload = {
                'replyToken':event.reply_token,
                'messages':[{
                    "type":"text",
                    "text": '好吧 我就告訴你吧'
                    },
                    {
                    "type":"text",
                    "text": messages
                    }]
                }
            res=requests.post('https://api.line.me/v2/bot/message/reply',headers=headers,data=json.dumps(payload))
            print(res.text)
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='我說\n你目前啥事都沒完成啊'))

    else:
        conn = sqlite.connect('%s/data/db/user_data.db'%(FileRoute))
        c = conn.cursor()
        c.execute('INSERT INTO %s (Memo) VALUES ("%s")'%(event.source.user_id, event.message.text))
        conn.commit()
        conn.close()

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='以記下筆記~'))

@handler.add(PostbackEvent)
def handle_postback(event):
    conn = sqlite.connect('%s/data/db/user_data.db'%(FileRoute))
    c = conn.cursor()
    c.execute('UPDATE %s SET status ="done" WHERE Memo ="%s"'%(event.source.user_id, event.postback.data))
    conn.commit()
    conn.close()

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='水喔 事情又少一件拉~'))
        
if __name__ == "__main__":
    app.run()
