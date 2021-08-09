# /usr/bin/python3.6
# -*- coding: utf-8 -*-
import json
import os
import re
import sys

import jenkins
import requests
from github import Github
from jira import JIRA

import ci_constants as CONSTANTS
from utils import *


def remove_file(file):
    if not os.path.exists(file):
        print("The file does not exist")
        return '-', '-'
    with open(file, 'r') as f:
        j = json.load(f)
        version_number = j['elements'][0]['versionName']
        versionCode = str(j['elements'][0]['versionCode'])
        if os.path.exists(file):
            os.remove(file)
        return version_number, versionCode


if __name__ == '__main__':
    status = sys.argv[1]
    issue = sys.argv[2]
    repo = sys.argv[3]
    GIT_BRANCH = sys.argv[4]
    GIT_COMMIT = sys.argv[5]
    pgy_apk_url = sys.argv[6]
    report_url = sys.argv[7]
    JOB_NAME = sys.argv[8]
    BUILD_NUMBER = sys.argv[9]
    BUILD_URL = sys.argv[10]
    recipient_default = sys.argv[11]
    recipient = sys.argv[12]

    jira_site = 'https://storehub.atlassian.net/browse'
    g = Github(CONSTANTS.GITHUB_TOKEN)
    rep = g.get_repo(repo)
    pr_num = int(GIT_BRANCH.split('-')[1])
    pr = rep.get_pull(pr_num)
    issue_branch = pr.head.ref

    version_get = None
    file = "/data/share/android__package/apk-beep-fat/output-metadata.json"
    version_number, versionCode = remove_file(file)

    features_failed = ''
    if issue_branch.startswith("release"):
        data = rep.get_branch(issue_branch).raw_data
        commit_info = data['commit']['commit']['message']
        text = format_message(
            job_name=JOB_NAME,
            source_branch=pr.head.ref,
            target_branch=pr.base.ref,
            status=status,
            version_number=version_number,
            versionCode=versionCode,
            pgy_url=pgy_apk_url,
            git_commit=GIT_COMMIT,
            commit_info=commit_info,
            report_url=report_url,
            build_url=BUILD_URL,
        )
        send_message(recipient_default, text)
    else:
        data = rep.get_branch(issue).raw_data
        commit_info = data['commit']['commit']['message']
        url = 'https://storehub.atlassian.net/rest/api/3/issue/{}'.format(issue)
        r = requests.get(url, auth=CONSTANTS.AUTH)
        get_id = r.json()['fields']['project']['id']
        print('get_id:' + get_id)
        assignee = r.json()['fields']['assignee']['displayName']

        text = format_message(
            job_name=JOB_NAME,
            jira_site=jira_site,
            source_branch=pr.head.ref,
            target_branch=pr.base.ref,
            status=status,
            version_number=version_number,
            versionCode=versionCode,
            pgy_url=pgy_apk_url,
            git_commit=GIT_COMMIT,
            commit_info=commit_info,
            report_url=report_url,
            build_url=BUILD_URL,
            assignee=assignee,
        )
        recipient = recipient if recipient != 'None' else recipient_default
        send_message(recipient, text)
