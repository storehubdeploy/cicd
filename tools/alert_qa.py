# /usr/bin/python
import sys
import json
import requests

def  send_message(recipient, text, PAGE_ACCESS_TOKEN):
    if 't_' in recipient:
        thread_type="thread_key"
    else:
        thread_type="id"

    data={
            "recipient":{thread_type:recipient},
            "message":{
                "text":text,
                }
            }
    post_data = json.dumps(data)
    print(post_data)
    url = "https://graph.facebook.com/me/messages"
    headers = {'Content-Type': 'application/json'}
    payload = {'access_token':PAGE_ACCESS_TOKEN}
    try:
        r = requests.post(url, headers=headers, params=payload, data=post_data)
        r.raise_for_status()
    except requests.RequestException as e:
        return e
    else:
        return r.json()
if __name__ == "__main__":
    PAGE_ACCESS_TOKEN = ''
    #recipient = ""
    text = sys.stdin.readline()

    print(text)

    recipient_default = sys.argv[1]
    recipient = sys.argv[2]
    print(recipient_default, recipient,text, PAGE_ACCESS_TOKEN)
    if 'True' in text:
        print('True')
        send_message(recipient, text, PAGE_ACCESS_TOKEN)
    else:
        send_message(recipient_default, text, PAGE_ACCESS_TOKEN)
