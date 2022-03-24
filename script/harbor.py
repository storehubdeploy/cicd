import requests

# from requests.api import get
from requests.auth import HTTPBasicAuth


header = {
        'Content-Type': 'application/json'
}

auth = HTTPBasicAuth('admin', 'C7cKwnrS1GjTBantBXAV')

def get_project_id(baseUrl):
    # data = {}
    page = 1
    page_size = 20
    resp  = requests.get(baseUrl, params={'page_size': page_size, 'page': page}, headers=header, auth=auth)
    content = resp.json()
    return [item['project_id'] for item in content]
    # for item in content:
    #     data['project_name'] = item['name']
    #     data['project_id'] = item['project_id']

def get_project_name(baseUrl):
    page = 1
    page_size = 20
    resp  = requests.get(baseUrl, params={'page_size': page_size, 'page': page}, headers=header, auth=auth)
    content = resp.json()
    return [item['name'] for item in content]

def get_images_of_pj(url):
    
    def help(x):
        x['scan_overview'] != None
    resp = requests.get(url, params={'detail': 'true'}, headers=header, auth=auth)
    data = resp.json()
    # print(data)
    # arr = filter(help,data)
    try:
        sorted(data, key=lambda x: x['scan_overview']['creation_time'], reverse=True)
    # [print(i) for i in arr]
    except KeyError:
        pass
    if len(data) > 10:
        for i in data[10:]:
            delete_image(url, i['name'])

def delete_image(url, name):
    baseUrl = url + "/" + name

    resp = requests.delete(baseUrl, headers=header, auth=auth) 
    if resp.status_code == 200:
        print('ok')

def get_chart_of_pj(url):
    resp = requests.get(url, headers=header, auth=auth)
    return [i['name'] for i in resp.json()]

def get_versions_of_chart(url):
    resp = requests.get(url, headers=header, auth=auth)
    result = resp.json()
    if len(result) > 10:
        for i in result[10:]:
            delete_chart_version(url, i["version"])

def delete_chart_version(url, version):
    resp = requests.delete(url+'/'+version,headers=header, auth=auth)
    if resp.status_code == 200:
        print("ok")

def get_repositories(baseUrl,p_id):
    page = 1
    page_size = 20
    while True:
        resp = requests.get(baseUrl, params={'page_size': page_size, 'page': page, 'project_id': p_id}, headers=header, auth=auth)
        data = resp.json()
        if data:
            for item in data:
                print(item['name'])
                yield item['name']
            page += 1
        else:
            break 

if __name__ == "__main__":

    # store = get_project_id("http://harbor.mymyhub.com/api/projects"
    # for i in store:
    #     for name in get_repositories("http://harbor.mymyhub.com/api/repositories", i):
    #         # if name != "fat/backoffice-v1-web":
    #         get_images_of_pj("http://harbor.mymyhub.com/api/repositories/{}/tags".format(name))


    names = get_project_name("http://harbor.mymyhub.com/api/projects")
    for name in names:
        result = get_chart_of_pj("https://harbor.mymyhub.com/api/chartrepo/{}/charts".format(name))
        for i in result:
           print(name, i)
           get_versions_of_chart("https://harbor.mymyhub.com/api/chartrepo/{0}/charts/{1}".format(name, i))
