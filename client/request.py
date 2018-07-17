# importing the requests library
import requests

def sendRequest(url):
    # getting response object
    r = requests.get(url)

    # extracting data in json format
    data = r.text

    print(data)

extension = raw_input("enter extension: ")
# URL endpoint
URL = "http://172.20.10.2:8081/" + extension

if extension.startswith("get-"):
    for i in range(10000):
        sendRequest(URL)
elif extension.startswith("post-"):
    print 'post'
else:
    sendRequest(URL)
