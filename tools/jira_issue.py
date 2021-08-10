# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
from jira import JIRA
import re
import sys, os
import json
import requests
from github import Github
import jenkins

# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
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


def get_pro_version(project_info, pro_version_list):
    for pro in project_info:
        pro_version_dict = {}
        if pro['key'] in new_projects:
            pass
        else:
            #print(pro)
            pro_list.append(pro)
            #jra = jira.project('CRM')
            jra = jira.project('{}'.format(pro['key']))
            components = jira.project_components(jra)
            #print([c.name for c in components])
            versions = jira.project_versions(jra)
            #print(versions)
            r = requests.get('https://storehub.atlassian.net/rest/api/3/project/{}/versions'.format(int(pro['id'])), auth=("congyu.li@storehub.com", "bHvvtsw6LZ8LLgwfmS5V64FE"))
            result = r.json()
            version_list = []
            if r.status_code == 200 and result:
                result_list = result
                for version in result_list:
                    if version['released']:
                        pass
                    else:
                        #print(version)
                        version_list.append(version)
            else:
                pass
                #print('project {} does not have a release'.format(pro))
            pro_version_dict['project'] = pro
            pro_version_dict['version'] = version_list
            if pro_version_dict:
                pro_version_list.append(pro_version_dict)
    return pro_version_list

def  remove_file(file):
    with open(file, 'r') as f:
        j = json.load(f)
        version_number = j[0]['apkData']['versionName']
        versionCode = str(j[0]['apkData']['versionCode'])
        print(version_number)
        if os.path.exists(file):
            os.remove(file)
        else:
            print("The file does not exist")
        return version_number, versionCode

def get_error(repo):
    if repo == "storehubnet/pos-v3-mobile":
        server = jenkins.Jenkins('https://jenkins.shub.us', username='jenkins_pub', password='AW_.AMucEE2QLmvFLpDi')
        last_build_number = server.get_job_info('qa_automation_UI-test')['lastCompletedBuild']['number']
        build_info = server.get_build_info('qa_automation_UI-test', last_build_number)
        console_output = server.get_build_console_output('qa_automation_UI-test', last_build_number)
        features_failed_number = int(re.findall("\d failed", console_output)[0].split()[0])
        if features_failed_number > 0:
            features_failed = "{} features failed".format(features_failed_number)
            return features_failed


if __name__ == '__main__':
    jira = JIRA('https://storehub.atlassian.net', basic_auth=(name, password)

    # Get all projects viewable by anonymous users.
    projects = jira.projects()
    new_projects = ['ARC', 'AUT', 'CRRN', 'DS', 'DOP', 'INF', 'LOG', 'PB', 'PS']
    # print(projects)

    project_info = [{"name": p.name, "id": p.id, "key": p.key} for p in reversed(projects)]
    print(project_info)
    pro_list = []
    pro_version = []
    pro_version_list = []

    status = sys.argv[1]
    issue = sys.argv[2]
    repo = sys.argv[3]
    GIT_BRANCH = sys.argv[4]
    GIT_COMMIT = sys.argv[5]
    pgy_url = sys.argv[6]
    report_url = sys.argv[7]
    JOB_NAME = sys.argv[8]
    BUILD_NUMBER = sys.argv[9]
    BUILD_URL = sys.argv[10]
    recipient_default = sys.argv[11]
    recipient = sys.argv[12]
    PAGE_ACCESS_TOKEN = 'DQVJ1RFhaWUxaNlRyZAHQ0bVZAKYzlPMUxZAY1ZAHNzROamxzN2FnYW9EMk9OWkFYYnZAtdlRzazZARbndqMzZAYWjljTGQxWHp6WHU0OEVfckV1RkdBcEdieFNILVhlbDJYZAUtqQWY2UTBCaGxGc182YS1saWdvTVoyd3h6SmFla0xCYU5yV3ZA6VTdPVkQ4a2RmNGxkWjFtUTN4Si1tRnBZANzF2N05mdXRLN2I3Mk1XOGVGb3N5cUdYaDFtSjVGdjRFV20wVWhSTzJB'
    jira_site = 'https://storehub.atlassian.net/browse'
    g = Github("token")
    rep = g.get_repo(repo)
    pr_num = int(GIT_BRANCH.split('-')[1])
    pr = rep.get_pull(pr_num)
    issue_branch = pr.head.ref
    #print(issue_branch)
    #version_number, versionCode = '', ''
    version_get = None
    features_failed = ''
    file = "/data/share/android__package/apk-rnpos-fat/output.json"
    version_number, versionCode = remove_file(file)
    if issue_branch.startswith("release"):
        data = rep.get_branch(issue_branch).raw_data
        commit_info = data['commit']['commit']['message']
        text = "App JOB_NAME: {}\n\n".format(JOB_NAME)  + "Status: {}\n\n".format(
            status) + "Source Branch: {}\n\n".format(pr.head.ref) + "Target Branch: {}\n\n".format(
            pr.base.ref) + "Build: {}_{}\n\n".format(version_number, versionCode) + "APP_URL: {}\n\n".format(
            pgy_url) + "Revison: {} {}\n\n".format(GIT_COMMIT, commit_info) + "REPORT_URL: {}\n\n".format(
            report_url) + "BUILD_URL: {}\n\n".format(BUILD_URL)
        send_message(recipient_default, text, PAGE_ACCESS_TOKEN)
    else:
        data = rep.get_branch(issue).raw_data
        commit_info = data['commit']['commit']['message']
        url = 'https://storehub.atlassian.net/rest/api/3/issue/{}'.format(issue)
        r = requests.get(url, auth=('congyu.li@storehub.com', 'bHvvtsw6LZ8LLgwfmS5V64FE'))
        get_id = r.json()['fields']['project']['id']
        assignee = r.json()['fields']['assignee']['displayName']
        if r.json()['fields']['fixVersions']:
            version_get = r.json()['fields']['fixVersions'][0]['name']
        pro_version_list = get_pro_version(project_info, pro_version_list)
        #print(pro_version_list)

        for i in pro_version_list:
            ver_list = []
            id = i['project']['id']
            if version_get == None and id == get_id:
                text = "App JOB_NAME: {}\n\n".format(JOB_NAME) + "Ticket: {}/{}\n\n".format(jira_site, pr.head.ref) + "Status: {}\n\n".format(status) + "Source Branch: {}\n\n".format(pr.head.ref) + "Target Branch: {}\n\n".format(pr.base.ref) + "Build: {}_{}\n\n".format(version_number, versionCode) + "APP_URL: {}\n\n".format(pgy_url) + "Revison: {} {}\n\n".format(GIT_COMMIT, commit_info) + "REPORT_URL: {}\n\n".format(report_url) + "BUILD_URL: {}\n\n".format(BUILD_URL) + "Assignee: {}\n\n".format(assignee)
                send_message(recipient_default, text, PAGE_ACCESS_TOKEN)
            else:
                ver_list =  i['version']
                for v in ver_list:
                    if v['name'] == version_get:
                        project_name = i['project']['key']
                        id = v['id']
                        url = "https://storehub.atlassian.net/projects/{}/versions/{}/tab/release-report-all-issues".format(project_name, id)
                        #print("issue_list: {}".format(url), has_version)
                        text = "App JOB_NAME: {}\n\n".format(JOB_NAME) + "Ticket: {}/{}\n\n".format(jira_site,
                            pr.head.ref) + "Status: {}\n\n".format(status) + "Source Branch: {}\n\n".format(pr.head.ref) + "Target Branch: {}\n\n".format(
                            pr.base.ref) + "Build: {}_{}\n\n".format(version_number, versionCode) + "APP_URL: {}\n\n".format(
                            pgy_url) + "Revison: {} {}\n\n".format(GIT_COMMIT, commit_info) + "REPORT_URL: {}\n\n".format(
                            report_url) + "BUILD_URL: {}\n\n".format(BUILD_URL) + "Assignee: {}\n\n".format(assignee)
                        send_message(recipient, text, PAGE_ACCESS_TOKEN)
