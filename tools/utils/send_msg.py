# /usr/bin/python3.6
# -*- coding: utf-8 -*-
import json
import sys,os
from optparse import OptionParser

sys.path.append(os.path.dirname(sys.path[0]))
import ci_constants as CONSTANTS
import requests


def send_message(recipient, text):
    if 't_' in recipient:
        thread_type = "thread_key"
    else:
        thread_type = "id"

    data = {
        "recipient": {thread_type: recipient},
        "message": {
            "text": text,
        },
    }
    post_data = json.dumps(data)
    url = CONSTANTS.WORKPLACE_URL
    headers = {'Content-Type': 'application/json'}
    payload = {'access_token': CONSTANTS.WORKPLACE_TOKEN}

    try:
        r = requests.post(url, headers=headers, params=payload, data=post_data)
        r.raise_for_status()
    except requests.RequestException as e:
        #print('recipient:' + recipient)
        #print('text:' + text)
        print(str(e))
        return e
    else:
        return r.json()


if __name__ == '__main__':
    parser=OptionParser()
    parser.add_option("--r", dest="recipient")
    parser.add_option("--t", dest="text")
    (options, args) = parser.parse_args()

    send_message(options.recipient, options.text