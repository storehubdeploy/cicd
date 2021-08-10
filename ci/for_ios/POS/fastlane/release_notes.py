#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, json
import requests

if __name__ == "__main__":
    url ='http://apollo-pro.shub.us'

    r = requests.get("{0}/configfiles/json/pos/default/apple".format(url))
    RELEASE_NOTES=r.json()['RELEASE_NOTES']+'\n'
    with open('./fastlane/metadata/en-US/release_notes.txt', 'w') as f:
       f.write(str(RELEASE_NOTES.encode('utf-8')))
