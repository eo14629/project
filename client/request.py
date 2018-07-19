# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs

import requests
import subprocess
from subprocess import call

def send404Request(url):
    r = requests.get(url)
    data = r.text
    print(data)

def get(url):
    sendGetRequest(url, 12000, "file1")
    sendGetRequest(url, 12000, "file10")
    sendGetRequest(url, 12000, "file100")
    sendGetRequest(url, 12000, "file300")
    sendGetRequest(url, 12000, "file700")
    sendGetRequest(url, 10000, "file1000")
    sendGetRequest(url, 8000, "file3000")
    sendGetRequest(url, 8000, "file6000")
    sendGetRequest(url, 7500, "file10000")
    sendGetRequest(url, 2000, "file100000")
    sendGetRequest(url, 1200, "file500000")
    sendGetRequest(url, 600, "file1000000")
    
def post(url):
    sendPostRequest(url, 12000, "txt1")
    sendPostRequest(url, 12000, "txt10")
    sendPostRequest(url, 12000, "txt100")
    sendPostRequest(url, 12000, "txt300")
    sendPostRequest(url, 12000, "txt700")
    sendPostRequest(url, 10000, "txt1000")
    sendPostRequest(url, 8000, "txt3000")
    sendPostRequest(url, 8000, "txt6000")
    sendPostRequest(url, 7500, "txt10000")
    sendPostRequest(url, 2000, "txt100000")
    sendPostRequest(url, 1200, "txt500000")
    sendPostRequest(url, 600, "txt1000000")
    
def sendGetRequest(url, repeat, file_extension):
    for i in range(5):
        energyDataFile = open('getdata' + file_extension + 'r' + str(i+1) + '.csv','w')
        subprocess.Popen("cat /dev/ttyUSB0 >> getdata" + file_extension + "r" + str(i+1) + ".csv",shell=True, stdout=energyDataFile)
        for j in range(repeat):
            r = requests.get(url + file_extension)
            data = r.text
            #~ print(data)
        energyDataFile.close()


def sendPostRequest(url, repeat, filename):
    postfile = open("./" + filename,'rb')
    for i in range(5):
        energyDataFile = open('postdata' + filename + 'r' + i + '.csv','w')
        subprocess.Popen("cat /dev/ttyUSB0 >> postdata" + filename + "r" + str(i+1) + ".csv",shell=True, stdout=energyDataFile)
        for j in range(repeat):
            r = requests.post(url, data = postfile.read())
            post_response = r.text
            print(post_response)
        energyDataFile.close()
    postfile.close()

# start point

extension = raw_input("enter extension: ")
URL = "http://172.20.10.2:8081/" + extension

if extension.startswith("get-"):
    get(URL)
elif extension.startswith("post-"):
    post(URL)
else:
    send404Request(URL)

