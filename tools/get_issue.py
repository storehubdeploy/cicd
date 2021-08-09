# /usr/bin/python3.6
import sys
from jira import JIRA
import requests
import re
from github import Github

jira = JIRA('https://storehub.atlassian.net', basic_auth=("congyu.li@storehub.com", "bHvvtsw6LZ8LLgwfmS5V64FE"))
g = Github("b62038c258e1905eab0431ae082a6f32cfd25a83")
repo = g.get_repo(sys.argv[1])
pr_num = int(sys.argv[2].split('-')[1])
pr = repo.get_pull(pr_num)

print(pr.head.ref)
