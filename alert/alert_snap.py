#!/usr/bin/python3
import requests
import json
import argparse



def send_message(url, data):
    header = {
        "Content-Type": "application/json"
    }
    data = json.dumps(data)
    response = requests.post(url, data=data, headers=header)
    return response.status_code


if __name__ == "__main__":
    baseurl = "https://chatserver.k8s.shub.us/storehub?source=jenkins&group_id=t_4758297520905463"
    # send_message(baseurl, {"job_name": "web-api", "message": "the jenkins job merge branch master to release with conflicts"})
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-e","--env", help="the environment value", type=str, required=True)
    #parser.add_argument("-j","--job", help="the jenkins job name", type=str, required=True)
    # parser.add_argument("-t", "--type",help="is github or jenkins", type=str, required=True)
    #args = parser.parse_args()
    message = "S3 Snapshots upload succeed"
    data = {"message": message}
    send_message(baseurl, data)
