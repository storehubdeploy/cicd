#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys
import argparse
import requests
import subprocess
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = False)
    parser.add_argument("--app", action = 'store', dest = 'app',
                        required=True
                        )
    parser.add_argument("--env", action = 'store', dest = 'env',
                        required=True
                        )
    parser.add_argument("-t", action = 'store', dest = 'recipient',
                        required=True
                        )
    args = parser.parse_args()
    
    app = args.app
    env = args.env
    recipient = args.recipient

    

    url= 'http://3.0.223.114:9300'

    cmd = 'git log -1 --pretty=format:%s'
    description = subprocess.getoutput(cmd)

    data = {
           "recipient":recipient,
           "message":{"App": app,"Env": env,"Branch": os.getenv("GIT_BRANCH"),"Revision":os.getenv("GIT_COMMIT"),description:""}
           }
    r=requests.post(url,json=data)
    #print(r.json())
