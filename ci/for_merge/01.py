#!/usr/bin/env python3
# coding:utf-8
"""
  Author  : mingdez
  Dtae    : 201904
"""
import os, sys, time, json
sys.path.append("/data/ops/ci/libs")
from common import print_color

def merge_record():
    # pip3 install python-jenkins
    import jenkins
    import logging
    job_name   = os.getenv("JOB_NAME")
    current_id = os.getenv("BUILD_NUMBER")
    git_url    = os.getenv("GIT_URL")

    log_name='/data/logs/jenkins/%s.log' % (job_name)
    logging.basicConfig(level=logging.INFO,filename=log_name, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("Auto_Merge")
    user_id   = 'jenkins_pub'
    api_token = 'admin@#098'
    url       = 'https://jenkins.shub.us'
    server = jenkins.Jenkins( url, username=user_id, password=api_token)
    logger.info('>>> Start')
    output = server.get_build_console_output(job_name, int(current_id))
    to_revision,from_revision="",""
    for line in output.split('\n'):
        if 'Checking out Revision' in line:
            to_revision = line.split()[3]
        if 'Merging Revision' in line:
            from_revision = line.split()[2]
        if to_revision and from_revision:
            break
    result              = {}
    result['git_url'        ] = git_url
    result['build_url'      ] = "https://jenkins.shub.us/job/{}/{}/console".format(job_name,current_id)
    if from_revision:
        result['from_revision'  ] = from_revision
    if to_revision:
        result['to_revision'    ] = to_revision
    result['date'           ] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    logger.info(">>> {}".format(result))
    logger.info('>>> Finish')
    return result

if __name__ == "__main__":
    merge_record()
