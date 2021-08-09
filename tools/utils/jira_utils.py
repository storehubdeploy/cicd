# /usr/bin/python3.6
# -*- coding: utf-8 -*-
import json

import ci_constants as CONSTANTS
import requests

from jira import JIRA


def get_all_projects():
    jira = JIRA(
        'https://storehub.atlassian.net',
        basic_auth=CONSTANTS.AUTH,
    )

    projects = jira.projects()
    if projects.__len__ == 0:
        print('get_all_projects returns empty!')
    return projects


def get_project_version(projects):
    pro_version_list = []
    filter_projects = ['ARC', 'AUT', 'CRRN', 'DS', 'DOP', 'INF', 'LOG', 'PB', 'PS']

    project_info = [
        {"name": p.name, "id": p.id, "key": p.key} for p in reversed(projects)
    ]

    for pro in project_info:
        pro_version_dict = {}
        if pro['key'] in filter_projects:
            pass
        else:
            # jra = jira.project('CRM')
            # jra = jira.project('{}'.format(pro['key']))
            # components = jira.project_components(jra)
            # print([c.name for c in components])
            # versions = jira.project_versions(jra)
            # print(versions)
            r = requests.get(
                'https://storehub.atlassian.net/rest/api/3/project/{}/versions'.format(
                    int(pro['id'])
                ),
                auth=CONSTANTS.AUTH,
            )
            result = r.json()
            version_list = []
            if r.status_code == 200 and result:
                result_list = result
                for version in result_list:
                    if version['released']:
                        pass
                    else:
                        # print(version)
                        version_list.append(version)
            else:
                pass
                # print('project {} does not have a release'.format(pro))
            pro_version_dict['project'] = pro
            pro_version_dict['version'] = version_list
            if pro_version_dict:
                pro_version_list.append(pro_version_dict)
    if pro_version_list.__len__ == 0:
        print('get_project_version returns empty!')

    return pro_version_list
