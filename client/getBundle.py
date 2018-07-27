# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs

import requests
import time
import sys, getopt

URL = "http://192.168.0.34:8082/"

def wrongExtension(path):
    r = requests.get(URL + path)
    data = r.text
    print(data)

def createURL(path, req_repeats):
    url = URL
    for req_repeat in range(req_repeats):
        extension = path
        extension += "&"
        url += extension
    url = url[:-1]
    return url

def sendGetRequest(url, repeat):
    # t_start = time.time()
    for j in range(repeat):
        receive = requests.get(url)
        data = receive.text
        print data
    # t_end = time.time()
    # printDuration(t_end-t_start)

def printDuration(time):
    for i in range(40):
        for j in range(i):
            print time, 's'
        print("...")

def direct(path, req_repeats):
    if path.startswith("get-"):
        url = createURL(path, req_repeats)
        # print "url: ", url
        sendGetRequest(url, 1)
    else:
        wrongExtension(path)

def main(argv):
    # need the path, and the number of get repeats.
    # later will need the number of actual repeats
    path = ''
    req_repeats = 0
    try:
        optns, args = getopt.getopt(argv, "hp:r:",["path=","req_repeats="])
    except getopt.GetoptError:
        print "Usage: getBundle.py -p <path excluding preceeding'/'> -r <number of repeat requests>"
        sys.exit(2)
    for optn, arg in optns:
        if optn == '-h':
            print "Usage: getBundle.py -p <path excluding preceeding'/'> -r <number of repeat requests>"
            sys.exit()
        elif optn in ("-p","--path"):
            path = arg
        elif optn in ("-r","--req_repeats"):
            req_repeats = int(arg)
    print "path: ", path, "\nreq_repeats: ", req_repeats
    direct(path, req_repeats)

if __name__ == "__main__":
    main(sys.argv[1:])
