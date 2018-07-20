# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs
# Command to track the energy: cat /dev/ttyUSB0 >> monitor.csv

import requests
import subprocess
import time
from subprocess import call

def send404Request(url):
    r = requests.get(url)
    data = r.text
    print(data)

def get(url):
    sendGetRequest(url, 6000, "file1")
    sendGetRequest(url, 6000, "file10")
    sendGetRequest(url, 6000, "file100")
    sendGetRequest(url, 6000, "file300")
    sendGetRequest(url, 6000, "file700")
    sendGetRequest(url, 5000, "file1000")
    sendGetRequest(url, 4000, "file3000")
    sendGetRequest(url, 4000, "file6000")
    sendGetRequest(url, 4000, "file10000")
    sendGetRequest(url, 1000, "file100000")
    sendGetRequest(url, 600, "file500000")
    sendGetRequest(url, 300, "file1000000")
    
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
    for i in range(5):
        timeFile = open('times/timestamp' + file_extension + 'r' + str(i+1) + '.csv','w')
        energyDataFile = open('data/getdata' + file_extension + 'r' + str(i+1) + '.csv','w')
        subprocess.Popen("cat /dev/ttyUSB0 >> data/getdata" + file_extension + "r" + str(i+1) + ".csv",shell=True, stdout=energyDataFile)
        t_start = time.time()
        for j in range(repeat):
            r = requests.get(url + file_extension)
            data = r.text
            #~ print(data)
        t_end = time.time()
        timeFile.write(str(t_end-t_start))
        energyDataFile.close()
        timeFile.close()

def sendPostRequest(url, repeat, filename):
    postfile = open("./" + filename + ".txt",'rb')
    HTTPbody = postfile.read()
    postfile.close()
    for i in range(5):
        timeFile = open('times/timestamp' + filename + 'r' + str(i+1) + '.csv','w' )
        energyDataFile = open('data/postdata' + filename + 'r' + str(i+1) + '.csv','w')
        subprocess.Popen("cat /dev/ttyUSB0 >> data/postdata" + filename + "r" + str(i+1) + ".csv",shell=True, stdout=energyDataFile)
        t_start = time.time()
        for j in range(repeat):
            r = requests.post(url, data = HTTPbody)
            post_response = r.text
            #~ print(post_response)
        t_end = time.time()
        timeFile.write(str(t_end-t_start))
        energyDataFile.close()
        timeFile.close()

extension = raw_input("enter extension: ")
URL = "http://192.168.0.34:8081/" + extension

if extension.startswith("get-"):
    get(URL)
elif extension.startswith("post-"):
    post(URL)
else:
    send404Request(URL)

