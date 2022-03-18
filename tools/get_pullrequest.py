import requests

url = "https://api.github.com/repos/storehubnet/logistics-domain-svc/pulls"

payload={}
headers = {
  'Authorization': 'token '
}

response = requests.request("GET", url, headers=headers, data=payload)

for pr in response.text:
    print(pr)

