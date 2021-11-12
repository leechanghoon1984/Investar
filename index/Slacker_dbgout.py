from slacker import Slacker
from datetime import datetime

import requests
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

myToken = "xoxb-1952383700611-1937427975911-chjYk26M3GQqRZZiicFLYTmI"

def dbgout(message):
  print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
  strbuf = datetime.now().strftime('[%m/%d %H:%M:%S]') + message
  post_message(myToken,"#stock", strbuf)

dbgout('This is test log')
