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
        status = emoji.emojize(':sparkles: success')
        text = (
                "Project: {}\n\n".format(job_name)
                + "Status: {}\n\n".format(status)
                + "Jira Ticket: {}/{}\n\n".format(jira_site, source_branch)
                + "Pull Request: {} -> {}\n\n".format(source_branch, target_branch)
                + "APP_URL: {}\n\n".format(pgy_url)
                + "Assignee: {}\n\n".format(assignee)
        )
    else:
        message = status
        status = emoji.emojize(':smiling_face_with_horns: failed')

        if jira_site == '':
            text = (
                    "Project: {}\n\n".format(job_name)
                    + "Status: {}\n\n".format(status)
                    + "Error Message: {}\n\n".format(message)
                    + "Build Version: {}_{}\n\n".format(version_number, versionCode)
                    + "Pull Request: {} -> {}\n\n".format(source_branch, target_branch)
                    + "Jenkins URL: {}\n\n".format(build_url)
                    + "Assignee: {}\n\n".format(assignee)
            )
        else:
            text = (
                    "Project: {}\n\n".format(job_name)
                    + "Status: {}\n\n".format(status)
                    + "Error Message: {}\n\n".format(message)
                    + "Build Version: {}_{}\n\n".format(version_number, versionCode)
                    + "Pull Request: {} -> {}\n\n".format(source_branch, target_branch)
                    + "Jira Title: {}\n\n".format(summary)
                    + "Jira Ticket: {}/{}\n\n".format(jira_site, source_branch)
                    + "Jenkins URL: {}\n\n".format(build_url)
                    + "Assignee: {}\n\n".format(assignee)
            )
    return text

def format_message_new(
        status="",
        app="",
        source_branch="",
        target_branch="",
        commit_info="",
        version_number="",
        versionCode="",
        pgy_url="",
        report_url="",
        build_url="",
        s3_url="",
        jira_site="",
        assignee="",
        summary="",
):
    if status == 'success':
        status = emoji.emojize(':sparkles: Success')
        if app == "backoffice-v2-webapp":
            text = (
                    "Project: {}\n\n".format(app)
                    + "Status: {}\n\n".format(status)
                    + "Jira_Ticket: {}/{}\n\n".format(jira_site, source_branch)
                    + "Pull_Request: {} -> {}\n\n".format(source_branch, target_branch)
                    + "Assignee: {}\n\n".format(assignee)
            )
        else:
            text = (
                    "Project: {}\n\n".format(app)
                    + "Status: {}\n\n".format(status)
                    + "Jira_Ticket: {}/{}\n\n".format(jira_site, source_branch)
                    + "Pull_Request: {} -> {}\n\n".format(source_branch, target_branch)
                    + "S3_URL: {}\n\n".format(s3_url)
                    + "Assignee: {}\n\n".format(assignee)
            )

    else:
        message = status
        status = emoji.emojize(':smiling_face_with_horns: Failed!')
        report_name=""

        if "API test" in message:
            report_url=report_url+"qareport_api.html"
            report_name="ApiTest_report"
        elif "UI test" in message:
            report_url=report_url+"qareport_ui/index.html"
            report_name="UITest_report"

        if jira_site == '':
            if "Prepare env" in message or "Unit Test" in message or "SonarQube" in message or "Packaging" in message or app == "backoffice-v2-webapp":
                text = (
                        "Project: {}\n\n".format(app)
                        + "Status: {}\n\n".format(status)
                        + "Error_Message: {}\n\n".format(message)
                        + "Pull_Request: {} -> {}\n\n".format(source_branch, target_branch)
                        + "Commit_Info: {}\n\n".format(commit_info)
                        + "Jenkins_URL: {}\n\n".format(build_url)
                )
            else:
                text = (
                        "Project: {}\n\n".format(app)
                        + "Status: {}\n\n".format(status)
                        + "Error_Message: {}\n\n".format(message)
                        + "Build_Version: {}_{}\n\n".format(version_number, versionCode)
                        + "Pull_Request: {} -> {}\n\n".format(source_branch, target_branch)
                        + "Commit_Info: {}\n\n".format(commit_info)
                        + "Jenkins_URL: {}\n\n".format(build_url)
                        + "{}: {}\n\n".format(report_name,report_url)
                        + "S3_URL: {}\n\n".format(s3_url)
                        + "Assignee: {}\n\n".format(assignee)
                )
        else:
            if "Prepare env" in message or "Unit Test" in message or "SonarQube" in message or "Packaging" in message or app == "backoffice-v2-webapp":
                text = (
                        "Project: {}\n\n".format(app)
                        + "Status: {}\n\n".format(status)
                        + "Error_Message: {}\n\n".format(message)
                        + "Pull_Request: {} -> {}\n\n".format(source_branch, target_branch)
                        + "Commit_Info: {}\n\n".format(commit_info)
                        + "Jira_Title: {}\n\n".format(summary)
                        + "Jira_Ticket: {}/{}\n\n".format(jira_site, source_branch)
                        + "Jenkins_URL: {}\n\n".format(build_url)
                        + "Assignee: {}\n\n".format(assignee)
                )
            else:
                text = (
                        "Project: {}\n\n".format(app)
                        + "Status: {}\n\n".format(status)
                        + "Error_Message: {}\n\n".format(message)
                        + "Build_Version: {}_{}\n\n".format(version_number, versionCode)
                        + "Pull_Request: {} -> {}\n\n".format(source_branch, target_branch)
                        + "Commit_Info: {}\n\n".format(commit_info)
                        + "Jira_Title: {}\n\n".format(summary)
                        + "Jira_Ticket: {}/{}\n\n".format(jira_site, source_branch)
                        + "Jenkins_URL: {}\n\n".format(build_url)
                        + "{}: {}\n\n".format(report_name,report_url)
                        + "S3_URL: {}\n\n".format(s3_url)
                        + "Assignee: {}\n\n".format(assignee)
                )
    return text