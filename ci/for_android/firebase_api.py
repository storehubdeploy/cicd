#!/usr/bin/env python
"""
  Author  : mingdez
  Dtae    : 201901
"""
import argparse
import os
import requests
import io

from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/firebase.remoteconfig']

# [START retrieve_access_token]
def _get_access_token():
    file_path='/data/downloads/keys/firebase/{0}.json'.format(project)
    if not os.path.exists(file_path):
        print('{0} not exists'.format(file_path))
        sys.exit(1)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        file_path, SCOPES)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token
# [END retrieve_access_token]

def _get():
    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }
    resp = requests.get(REMOTE_CONFIG_URL, headers=headers)

    if resp.status_code == 200:
        with io.open('remote_config.json', 'wb') as f:
            f.write(resp.text.encode('utf-8'))

        print('Retrieved template has been written to remote_config.json')
        print('ETag from server: {}'.format(resp.headers['ETag']))
    else:
        print('Unable to get template')
        print(resp.text)

def _listVersions():
    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }
    resp = requests.get(REMOTE_CONFIG_URL + ':listVersions?pageSize=5', headers=headers)

    if resp.status_code == 200:
        print('Versions:')
        print(resp.text)
    else:
        print('Request to print template versions failed.')
        print(resp.text)

def _rollback(version):
    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }

    json = {
        "version_number": version
    }
    resp = requests.post(REMOTE_CONFIG_URL + ':rollback', headers=headers, json=json)

    if resp.status_code == 200:
        print('Rolled back to version: ' + version)
        print(resp.text)
        print('ETag from server: {}'.format(resp.headers['ETag']))
    else:
        print('Request to roll back to version ' + version + ' failed.')
        print(resp.text)

def _publish(etag):
    with io.open('remote_config.json', 'r', encoding='utf-8') as f:
        content = f.read()
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
        'If-Match': etag
    }
    resp = requests.put(REMOTE_CONFIG_URL, data=content.encode('utf-8'), headers=headers)
    if resp.status_code == 200:
        print('Template has been published.')
        print('ETag from server: {}'.format(resp.headers['ETag']))
    else:
        print('Unable to publish template.')
        print(resp.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    parser.add_argument('--etag')
    parser.add_argument('--version')
    parser.add_argument('--project')
    args = parser.parse_args()

    BASE_URL = 'https://firebaseremoteconfig.googleapis.com'
    REMOTE_CONFIG_ENDPOINT = 'v1/projects/' + args.project + '/remoteConfig'
    global REMOTE_CONFIG_URL
    REMOTE_CONFIG_URL = BASE_URL + '/' + REMOTE_CONFIG_ENDPOINT
    global project
    project=args.project

    if args.project and args.action and args.action == 'get':
        _get()
    elif args.project and args.action and args.action == 'publish' and args.etag:
        _publish(args.etag)
    elif args.project and args.action and args.action == 'versions':
        _listVersions()
    elif args.project and args.action and args.action == 'rollback' and args.version:
        _rollback(args.version)
    else:
        print('''Invalid command. Please use one of the following commands:
python configure.py --project==project_id --action=get
python configure.py --project==project_id --action=publish --etag=<LATEST_ETAG>
python configure.py --project==project_id --action=versions
python configure.py --project==project_id --action=rollback --version=<TEMPLATE_VERSION_NUMBER>''')

if __name__ == '__main__':
  main()
