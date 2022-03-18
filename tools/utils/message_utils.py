# /usr/bin/python3.6
# -*- coding: utf-8 -*-
import json

import ci_constants as CONSTANTS
import requests
import emoji


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
        print('recipient:' + recipient)
        print('text:' + text)
        print(str(e))
        return e
    else:
        return r.json()


def format_message(
    job_name='',
    jira_site='',
    source_branch='',
    target_branch='',
    status='',
    version_number='',
    versionCode='',
    pgy_url='',
    git_commit='',
    commit_info='',
    report_url='',
    build_url='',
    assignee='',
    summary='',
):
    if status == 'success':
        status = emoji.emojize(':sparkles::sparkles::sparkles::sparkles: success :grinning_face::grinning_face::grinning_face::grinning_face:')
    else:
        status = emoji.emojize(':smiling_face_with_horns::smiling_face_with_horns::smiling_face_with_horns::smiling_face_with_horns: failed :ghost::ghost::ghost::ghost::ghost:')

    if jira_site == '':
        text = (
            "App JOB_NAME: {}\n\n".format(job_name)
            + "Status: {}\n\n".format(status)
            + "Source Branch: {}\n\n".format(source_branch)
            + "Target Branch: {}\n\n".format(target_branch)
            + "Build: {}_{}\n\n".format(version_number, versionCode)
            + "APP_URL: {}\n\n".format(pgy_url)
            + "Revison: {} {}\n\n".format(git_commit, commit_info)
            + "REPORT_URL: {}\n\n".format(report_url)
            + "BUILD_URL: {}\n\n".format(build_url)
        )
    else:
        text = (
            "App JOB_NAME: {}\n\n".format(job_name)
            + "Title: {}\n\n".format(summary)
            + "Ticket: {}/{}\n\n".format(jira_site, source_branch)
            + "Status: {}\n\n".format(status)
            + "Source Branch: {}\n\n".format(source_branch)
            + "Target Branch: {}\n\n".format(target_branch)
            + "Build: {}_{}\n\n".format(version_number, versionCode)
            + "APP_URL: {}\n\n".format(pgy_url)
            + "Revison: {} {}\n\n".format(git_commit, commit_info)
            + "REPORT_URL: {}\n\n".format(report_url)
            + "BUILD_URL: {}\n\n".format(build_url)
            + "Assignee: {}\n\n".format(assignee)
        )
    return text
