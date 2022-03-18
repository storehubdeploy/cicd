#!/usr/bin/env python3.6
# -*- coding: UTF-8 -*-
"""
  Author  : storehub
  Dtae    : 202001
"""

import os, sys, json
import requests
from optparse import OptionParser
sys.path.append("/data/ops/ci/libs")
from common import print_color
import re
from github import Github
from jira import JIRA

def get_config(category, conf, version):
    if category == 'properties':
        release_dict = {}
        r = requests.get("{0}/configfiles/json/{1}/{2}/{3}".format(url, appid, cluster, namespace))
        if r.status_code == 200:
            release_dict = {k: v for k, v in r.json().items()}
        else:
            print_color(31, "==> Can't connect to %s" % url)
            sys.exit(1)
        # print(release_dict)
        if conf == 'channel':
            return release_dict.get(version)
        elif conf == 'qaapi_action':
            return release_dict['qaapi_action']
        elif conf == 'qaui_action':
            return release_dict['qaui_action']
        elif conf == 'channel_default':
            return release_dict['channel_default']
        elif conf == 'pgy_url':
            return release_dict['pgy_url']
        elif conf == 'pgy_apk_url':
            return release_dict['pgy_apk_url']
        elif conf == 'pgy_ios_url':
            return release_dict['pgy_ios_url']
        elif conf == 'report_url':
            return release_dict['report_url']



if __name__ == "__main__":
    appid = sys.argv[1]
    cluster = sys.argv[2]
    conf = sys.argv[3]
    url = 'http://apollo-fat.shub.us'
    namespace = 'application'
    category = 'properties'
    jira = JIRA('https://storehub.atlassian.net', basic_auth=("", ""))
    g = Github("")
    repo = g.get_repo(sys.argv[4])
    pr_num = int(sys.argv[5].split('-')[1])
    pr = repo.get_pull(pr_num)
    issue = pr.head.ref
    #print(issue)
    version = None
    config = ''
    if issue.startswith("release"):
        config = get_config(category, conf, version)
        print(config)
    else:
        url1 = 'https://storehub.atlassian.net/rest/api/3/issue/{}'.format(issue)
        r = requests.get(url1, auth=('', ''))
        print(r.json())
        if r.json()['fields']['fixVersions']:
            version = r.json()['fields']['fixVersions'][0]['name']
        else:
            version = None
        config = get_config(category, conf, version)
        print(config)
