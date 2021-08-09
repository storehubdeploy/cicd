import requests

url = "https://api.github.com/repos/storehubnet/logistics-domain-svc/pulls"

payload={}
headers = {
  'Authorization': 'token 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'
}

response = requests.request("GET", url, headers=headers, data=payload)

for pr in response.text:
    print(pr)

