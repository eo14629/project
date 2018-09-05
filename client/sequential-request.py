# Python program using the 'Requests' HTTP Request Python API
# Program sends HTTP requests sequentially to the main server - non-bundled
# Can send GET, POST or PUT requests.
# Same tests as with the Java Programs

import requests
import time
import sys, getopt
from memory_profiler import profile

URL = "http://172.20.10.2:8081/"

# sends off the HTTP GET requests SEQUENTIALLY for the files requested
@profile
def sendGetRequest(url, repeats, file_extensions):
    data = []
    t_start = time.time()
    for j in range(repeats):
        for file_extension in file_extensions:
            r = requests.get(url + file_extension)
            if r.status_code == 200:
                data.append(r.text)
            else:
                data.append("Fail. Status Code: " + str(r.status_code))
    t_end = time.time()
    # printDuration(t_end-t_start)
    printData(data)

# repeated code (ie similar to sendGetRequest) because code inside
# for loop needs to be minimal as the energy of this loop will be measured
def sendPostRequest(url, repeats, file_extensions):
    data = []
    postfiles = []
    for file_extension in file_extensions:
        f = open("./txt" + file_extension.split('-file')[1] + ".txt",'rb')
        postfiles.append(f.read())
        f.close()

    t_start = time.time()
    for j in range(repeats):
        for postfile, file_extension in zip(postfiles, file_extensions):
            print url + file_extension
            r = requests.post(url + file_extension, data = postfile)
            data.append(r.text)
    t_end = time.time()
    # printDuration(t_end-t_start)
    printData(data)

# repeated again.
def sendPutRequest(url, repeats, file_extensions):
    data = []
    putfiles = []
    for file_extension in file_extensions:
        f = open("./txt" + file_extension.split('-file')[1] + ".txt",'rb')
        putfiles.append(f.read())
        f.close()

    t_start = time.time()
    for j in range(repeats):
        for putfile, file_extension in zip(putfiles, file_extensions):
            r = requests.put(url + file_extension, data = putfile)
            data.append(r.text)
    t_end = time.time()
    # printDuration(t_end-t_start)
    printData(data)

def printDuration(time):
    for i in range(30):
        for j in range(i):
            print time, 's'
        print("...")

def printData(data):
    count = 1
    for el in data:
        print "data", count, " length = ", len(el)
        print "\ndata", count, " value = ", el, "\n\n"
        count += 1

# determine HTTP request METHOD from URL extension (recieved from cmd line)
def checkMethod(paths):
    t = ""
    types = []
    for path in paths:
        types.append(path.split("-")[0])
    if types.count(types[0]) != len(types):
        pass
    elif types[0] == "get" or types[0] == "post" or types[0] == "put":
        t = types[0]
    return t

# direct to the put, post  of get requests.
def direct(paths):
    repeats = 1
    try:
        repeats = int(paths[len(paths)-1])
    except Exception as e:
        print "Error: Last argument is the number of repeats (integer)"
        sys.exit(2)
    paths = paths[:-1]
    print "paths: ", paths
    print "repeats: ", repeats

    extension = checkMethod(paths)
    if not extension:
        print "Error: All files must start with either get- post- or put- followed by the desired file size in bytes"
        sys.exit(2)

    if extension.startswith("get"):
        sendGetRequest(URL, repeats, paths)
    elif extension.startswith("post"):
        sendPostRequest(URL, repeats, paths)
    elif extension.startswith("put"):
        sendPutRequest(URL, repeats, paths)

def main(argv):
    paths = []
    for i in range(len(sys.argv)-1):
        paths.append(str(sys.argv[i+1]))
    if len(paths) == 0:
        print "Usage: sequential-requests.py [-requests (e.g get-file1000)]... num_repeats"

        sys.exit(2)
    direct(paths)

if __name__ == "__main__":
    main(sys.argv[1:])
