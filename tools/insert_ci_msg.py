from optparse import OptionParser

import requests
import json


parser=OptionParser()
parser.add_option("--p_name", dest="project_name")
parser.add_option("--t_branch", dest="target_branch")
parser.add_option("--s_branch", dest="source_branch")
parser.add_option("--start", dest="start_time", default="")
parser.add_option("--end", dest="end_time", default="")
parser.add_option("--s_env", dest="status_env", default="faild")
parser.add_option("--s_ut", dest="status_unit_test", default="faild")
parser.add_option("--s_sonar", dest="status_sonar", default="faild")
parser.add_option("--s_pkg", dest="status_pkg", default="faild")
parser.add_option("--s_api", dest="status_api", default="faild")
parser.add_option("--s_ui", dest="status_ui", default="faild")
parser.add_option("--status", dest="status", default="faild")
parser.add_option("--error_msg", dest="error_msg", default="faild")
parser.add_option("--s3", dest="s3_pkg_url", default="null")
parser.add_option("--assignee", dest="assignee", default="null")
(options, args) = parser.parse_args()

url = "https://b2e5-137-59-100-182.ap.ngrok.io/add"

payload = json.dumps({
    "project_name": options.project_name,
    "target_branch": options.target_branch,
    "source_branch": options.source_branch,
    "start_time": options.start_time,
    "end_time": options.end_time,
    "status_env": options.status_env,
    "status_unit_test": options.status_unit_test,
    "status_sonar": options.status_sonar,
    "status_pkg": options.status_pkg,
    "status_api": options.status_api,
    "status_ui": options.status_ui,
    "status": options.status,
    "error_msg": options.error_msg,
    "s3_pkg_url": options.s3_pkg_url,
    "assignee": options.assignee
})

print(payload)
headers = {
    'Content-Type': 'application/json'
}

requests.request("POST", url, headers=headers, data=payload)