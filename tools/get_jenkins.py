import jenkins
import re
import sys
import datetime
from github import Github

g = Github("token")

server = jenkins.Jenkins('https://jenkins.shub.us', username='jenkins_pub', password='AW_.AMucEE2QLmvFLpDi')

p_name = sys.argv[1]
branch = sys.argv[2]
bucket = sys.argv[3]
print(branch)
repo = g.get_repo(sys.argv[4])
data = repo.get_branch(branch).raw_data
commit_info = data['commit']['commit']['message']
server.build_job('upload_pgy', {'apk_newname': p_name, 'bucket': bucket, 'branch': branch, 'commit_info': commit_info})
