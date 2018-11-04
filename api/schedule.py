import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from setting import *

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
                    "text": item,
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
                        "data": item
                    },
                    "flex": 1
                    }
                ]
            }
        ]
    return content

memo_dict = {}
sent_list = []
conn = sqlite.connect('%s/data/db/user_data.db'%(FileRoute))
c = conn.cursor()
user_id = c.execute("SELECT name FROM sqlite_master WHERE type='table'")
user_id = user_id.fetchall()
# print(user_id)
for item in user_id:
    memo = c.execute("SELECT Memo FROM %s WHERE status ='working'"%(item[0]))
    memo_dict['user_id'] = item[0]
    memo_dict['memo'] = []
    for item2 in memo.fetchall():
        memo_dict['memo'] += [item2[0]]
    sent_list += [memo_dict]
    memo_dict = {}
conn.commit()
conn.close()


print(sent_list[0]['memo'])
print(sent_list[0]['user_id'])
for item in sent_list:
    memo = item['memo']
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
                            "text": "欸欸 我說 你該為朕做些事了吧",
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
            'to':item['user_id'],
            'messages':[flex]
            }
        res=requests.post('https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(payload))
    else:
        None