# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs

import requests
import time
import sys, getopt
from memory_profiler import profile

def wrongExtension(url, repeats):
    r = requests.get(url)
    data = r.text
    print(data)

def get(url, repeats):
    # sendGetRequest(url, 3000, "file1")
    sendGetRequest(url, repeats, "file1000", "file6000", "file90000", "file100000")
    #~ sendGetRequest(url, 3000, "file100")
    #~ sendGetRequest(url, 3000, "file300")
    #~ sendGetRequest(url, 3000, "file700")
    #~ sendGetRequest(url, 2500, "file1000")
    # sendGetRequest(url, 1, "file3000")
    #~ sendGetRequest(url, 2000, "file6000")
    #~ sendGetRequest(url, 2000, "file10000")
    #~ sendGetRequest(url, 500, "file100000")
    #~ sendGetRequest(url, 300, "file500000")
    #~ sendGetRequest(url, 150, "file1000000")

def putpost(url, repeats):
    sendPutPostRequest(url, 3000, "txt1")
    #~ sendPutPostRequest(url, 3000, "txt10")
    #~ sendPutPostRequest(url, 3000, "txt100")
    #~ sendPutPostRequest(url, 3000, "txt300")
    #~ sendPutPostRequest(url, 3000, "txt700")
    #~ sendPutPostRequest(url, 2500, "txt1000")
    #~ sendPutPostRequest(url, 2000, "txt3000")
    #~ sendPutPostRequest(url, 2000, "txt6000")
    #~ sendPutPostRequest(url, 2000, "txt10000")
    #~ sendPutPostRequest(url, 500, "txt100000")
    #~ sendPutPostRequest(url, 300, "txt500000")
    #~ sendPutPostRequest(url, 150, "txt1000000")

@profile
def sendGetRequest(url, repeats, *file_extensions):
    t_start = time.time()
    for j in range(repeats):
        r = requests.get(url + file_extensions[0])
        data = r.text
        #~ print data
        #~ print r.status_code
        r = requests.get(url + file_extensions[1])
        data = r.text
        #~ print data
        #~ print r.status_code
        r = requests.get(url + file_extensions[2])
        data = r.text
        #~ print data
        #~ print r.status_code
        r = requests.get(url + file_extensions[3])
        data = r.text
        #~ print data
        #~ print r.status_code
    t_end = time.time()
    # printDuration(t_end-t_start)

def sendPutPostRequest(url, repeats, filename):
    postfile = open("./" + filename + ".txt",'rb')
    HTTPbody = postfile.read()
    postfile.close()

    # can change the post request line to a put simply by changing the word.
    t_start = time.time()
    for j in range(repeats):
        r = requests.post(url, data = HTTPbody)
        post_response = r.text
    t_end = time.time()
    printDuration(t_end-t_start)

def printDuration(time):
    for i in range(30):
        for j in range(i):
            print time, 's'
        print("...")

def main(argv):
    # extension = raw_input("enter extension: ")
    extension = "get-"
    URL = "http://192.168.0.34:8081/" + extension
    repeats = int(sys.argv[1])
    if extension.startswith("get-"):
        get(URL, repeats)
    elif extension.startswith("post-"):
        putpost(URL, repeats)
    else:
        wrongExtension(URL,repeats)

if __name__ == "__main__":
    main(sys.argv[1:])
