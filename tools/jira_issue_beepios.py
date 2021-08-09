# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
from jira import JIRA
import re
import sys, os
import json
import requests
from github import Github
import jenkins
import ci_constants as CONSTANTS
from utils import *

if __name__ == '__main__':
    projects = get_all_projects()

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
    g = Github("b62038c258e1905eab0431ae082a6f32cfd25a83")
    rep = g.get_repo(repo)
    pr_num = int(GIT_BRANCH.split('-')[1])
    pr = rep.get_pull(pr_num)
    issue_branch = pr.head.ref
    # print(issue_branch)
    version_number, versionCode = '', ''
    version_get = None
    # file = "/data/share/android__package/apk-beep-fat/output-metadata.json"
    # version_number, versionCode = remove_file(file)
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
        r = requests.get(
            url, auth=('nick.huang@storehub.com', 'MEf01OqNi2iBV7r22tFE9EC7')
        )
        get_id = r.json()['fields']['project']['id']
        assignee = r.json()['fields']['assignee']['displayName']
        if r.json()['fields']['fixVersions']:
            version_get = r.json()['fields']['fixVersions'][0]['name']
        pro_version_list = get_project_version(projects)

        for i in pro_version_list:
            ver_list = []
            id = i['project']['id']
            if version_get == None and id == get_id:
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
                send_message(recipient_default, text)
            else:
                ver_list = i['version']
                for v in ver_list:
                    if v['name'] == version_get:
                        project_name = i['project']['key']
                        id = v['id']
                        url = "https://storehub.atlassian.net/projects/{}/versions/{}/tab/release-report-all-issues".format(
                            project_name, id
                        )
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
