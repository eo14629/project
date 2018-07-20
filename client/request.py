# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs

import requests
import time

def wrongExtension(url):
    r = requests.get(url)
    data = r.text
    print(data)

def get(url):
    sendGetRequest(url, 6000, "file1")
    # sendGetRequest(url, 6000, "file10")
    # sendGetRequest(url, 6000, "file100")
    # sendGetRequest(url, 6000, "file300")
    # sendGetRequest(url, 6000, "file700")
    # sendGetRequest(url, 5000, "file1000")
    # sendGetRequest(url, 4000, "file3000")
    # sendGetRequest(url, 4000, "file6000")
    # sendGetRequest(url, 4000, "file10000")
    # sendGetRequest(url, 1000, "file100000")
    # sendGetRequest(url, 600, "file500000")
    # sendGetRequest(url, 300, "file1000000")

def post(url):
    sendPostRequest(url, 6000, "txt1")
    sendPostRequest(url, 6000, "txt10")
    sendPostRequest(url, 6000, "txt100")
    sendPostRequest(url, 6000, "txt300")
    sendPostRequest(url, 6000, "txt700")
    sendPostRequest(url, 5000, "txt1000")
    sendPostRequest(url, 4000, "txt3000")
    sendPostRequest(url, 4000, "txt6000")
    sendPostRequest(url, 400, "txt10000")
    sendPostRequest(url, 1000, "txt100000")
    sendPostRequest(url, 600, "txt500000")
    sendPostRequest(url, 300, "txt1000000")

def sendGetRequest(url, repeat, file_extension):
    t_start = time.time()
    for j in range(repeat):
        r = requests.get(url + file_extension)
        data = r.text
        #~ print(data)
    t_end = time.time()
    printDuration(t_end-t_start)

def sendPostRequest(url, repeat, filename):
    postfile = open("./" + filename + ".txt",'rb')
    HTTPbody = postfile.read()
    postfile.close()

    t_start = time.time()
    for j in range(repeat):
        r = requests.post(url, data = HTTPbody)
        post_response = r.text
        #~ print(post_response)
    t_end = time.time()
    printDuration(t_end-t_start)

def printDuration(time):
    for i in range(40):
        for j in range(i):
            print time, 's'
        print("...")

extension = raw_input("enter extension: ")
URL = "http://192.168.0.34:8081/" + extension

if extension.startswith("get-"):
    get(URL)
elif extension.startswith("post-"):
    post(URL)
else:
    wrongExtension(URL)
