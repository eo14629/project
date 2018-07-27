# Python program using the 'Requests' HTTP Request Python API
# Same tests as with the Java Programs

import requests
import time
import sys, getopt

URL = "http://192.168.0.34:8082/"

def printDuration(time):
    for i in range(40):
        for j in range(i):
            print time, 's'
        print("...")

def sendGetRequest(url, repeats):
    t_start = time.time()
    for j in range(repeats):
        receive = requests.get(url)
        data = receive.text
        print data
    t_end = time.time()
    printDuration(t_end-t_start)

# Creating the bundled URL to be sent to the Proxy server_response
# by using the correct parsing
def createURL(paths, total_paths):
    url = URL
    for p in range(total_paths):
        extension = paths[p]
        extension += "&"
        url += extension
    url = url[:-1]
    return url

# Converting the arguments to strings to be used for the URL and the
# final argument to be used for the number of repeats
def main(argv):
    paths = []
    repeats = 1
    for i in range(len(sys.argv)-1):
        paths.append(str(sys.argv[i+1]))
    try:
        repeats = int(paths[len(paths)-1])
    except Exception as e:
        print "Last argument should be a number. It is the number of repeats"
        sys.exit(2)
    paths = paths[:-1]
    print paths
    url = createURL(paths, len(paths))
    sendGetRequest(url, repeats)

if __name__ == "__main__":
    main(sys.argv[1:])
