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
    baseurl = "https://chatserver.k8s.shub.us/storehub?source=jenkins&group_id=t_2483107158381967"
    # send_message(baseurl, {"job_name": "web-api", "message": "the jenkins job merge branch master to release with conflicts"})


    message = "Warning! the Coverage of saving plan is below 90% , Pls Check!"
    data = {"message": message}
    send_message(baseurl, data)

