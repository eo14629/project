# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs

import requests

def sendRequest(url):
    r = requests.get(url)
    data = r.text
    print(data)

def sendGetRequest(url, repeat):
    for i in range(repeat):
        r = requests.get(url)
        data = r.text
        print(data)

def sendPostRequest(url, repeat, filecontents):
    for i in range(repeat):
        r = requests.post(url, data = filecontents)
        post_response = r.text
        print(post_response)

repeat = 1000
extension = raw_input("enter extension: ")
URL = "http://172.20.10.2:8081/" + extension

if extension.startswith("get-"):
    sendGetRequest(URL, repeat)
elif extension.startswith("post-"):
    f = open('./txt10.txt','rb')
    sendPostRequest(URL, repeat, f.read())
else:
    sendRequest(URL)
