# /usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
from jira import JIRA
import ci_constants as CONSTANTS

jira = JIRA(
    'https://storehub.atlassian.net',
    basic_auth=CONSTANTS.AUTH,
)

if __name__ == '__main__':
    get_issue = sys.argv[1]
    comments = sys.argv[2]
    label = sys.argv[3]

    if get_issue.startswith("release"):
        print('No ticket')
    else:
        # Get an issue.
        issue = jira.issue(get_issue)
        old_list = []
        if issue.fields.labels != None:
            old_list = issue.fields.labels
            if 'Not_ready' in old_list:
                old_list.remove('Not_ready')
            if 'Ready_For_Test' in old_list:
                old_list.remove('Ready_For_Test')
            if label in old_list:
                old_list.remove(label)

        old_list.append(label)
        jira.add_comment(issue, comments)
        issue.update(fields={"labels": old_list})
