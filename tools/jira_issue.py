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
from optparse import OptionParser

import ci_constants as CONSTANTS
from utils import *

# TODO: it's not same structure as beep android
# not use now
def get_apk_info(file):
    if not os.path.exists(file):
        print("The file does not exist: " + file)
        return '-', '-'
    with open(file, 'r') as f:
        j = json.load(f)
        version_number = j['elements'][0]['versionName']
        versionCode = str(j['elements'][0]['versionCode'])
        s3_url = str(j['S3_URL'])
        if os.path.exists(file):
            os.remove(file)
        return version_number, versionCode, s3_url


if __name__ == '__main__':
    jira_site = 'https://storehub.atlassian.net/browse'

    # init parameters
    parser=OptionParser()
    parser.add_option("--status"           , dest="status", default="false")                    # Pipeline run status
    parser.add_option("--repo"             , dest="repo", default="storehubnet/pos-v3-mobile")  # github repo
    parser.add_option("--pr_branch"        , dest="PR_BRANCH")                                 # PR-1613
    parser.add_option("--pgy_url"          , dest="pgy_apk_url")                                # pgyer url
    parser.add_option("--report_url"       , dest="report_url")
    parser.add_option("--app"              , dest="app", default="RN POS")
    parser.add_option("--build_url"        , dest="BUILD_URL")                                  # PR jenkins job url
    parser.add_option("--recipient_default", dest="recipient_default", default="t_4690699114301828")
    parser.add_option("--recipient"        , dest="recipient", default="")
    parser.add_option("--s3"               , dest="s3_url", default="null")
    parser.add_option("--versionCode"      , dest="versionCode", default="null")
    parser.add_option("--versionNum"       , dest="versionNum", default="null")
    (options, args) = parser.parse_args()

    # get github message, use 'repo' and 'PR_BEANCH'
    g = Github(CONSTANTS.GITHUB_TOKEN)
    rep = g.get_repo(options.repo)
    pr_num = int(options.PR_BRANCH.split('-')[1])
    pr = rep.get_pull(pr_num)

    # github parameters
    source_branch = pr.head.ref
    target_branch = pr.base.ref  # master
    data = rep.get_branch(source_branch).raw_data
    commit_info = data['commit']['commit']['message']

    # print("\n\n"+options.s3,options.status,options.repo, options.PR_BRANCH, options.pgy_apk_url, options.report_url, options.app, options.BUILD_URL,
    #       options.recipient_default, options.recipient ,source_branch, target_branch, commit_info, versionNum, versionCode, s3_url)

    if source_branch.startswith("release"):
        text = format_message_new(
            status=options.status,
            app=options.app,
            source_branch=source_branch,
            target_branch=target_branch,
            commit_info=commit_info,
            version_number=options.versionNum,
            versionCode=options.versionCode,
            pgy_url=options.pgy_apk_url,
            report_url=options.report_url,
            build_url=options.BUILD_URL,
            s3_url=options.s3_url,
        )
        send_message(options.recipient_default, text)
    else:
        assignee, summary, project_id, fix_version = get_ticket_info(source_branch)
        print(">>>"+assignee, summary, project_id, fix_version)
        text = format_message_new(
            status=options.status,
            app=options.app,
            source_branch=source_branch,
            target_branch=target_branch,
            commit_info=commit_info,
            version_number=options.versionNum,
            versionCode=options.versionCode,
            pgy_url=options.pgy_apk_url,
            report_url=options.report_url,
            build_url=options.BUILD_URL,
            s3_url=options.s3_url,
            jira_site=jira_site,
            assignee=assignee,
            summary=summary,
        )
        recipient = options.recipient if options.recipient != 'None' else options.recipient_default
        send_message(recipient, text)

