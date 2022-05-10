#!/usr/bin/env python3.6
# -*- coding: UTF-8 -*-

from dotenv import dotenv_values
import os

path = os.path.join(os.path.dirname(__file__), 'ci.env')
config = dotenv_values(path)

# for c in config.items():
#     print(c)

JIRA_URL = config['JIRA_URL']
JIRA_USER = config['JIRA_USER']
JIRA_TOKEN = config['JIRA_TOKEN']
AUTH = (JIRA_USER, JIRA_TOKEN)

APOLLO_URL = config['APOLLO_URL']
APOLLO_USER = config['APOLLO_USER']
APOLLO_PASSWORD = config['APOLLO_PASSWORD']

GITHUB_URL = config['GITHUB_URL']
GITHUB_TOKEN = config['GITHUB_TOKEN']

JENKINS_URL = config['JENKINS_URL']
JENKINS_USER = config['JENKINS_USER']
JENKINS_PASSWORD = config['JENKINS_PASSWORD']

WORKPLACE_URL = config['WORKPLACE_URL']
WORKPLACE_TOKEN = config['WORKPLACE_TOKEN']

GOOGLE_PWD = config['GOOGLE_PWD']