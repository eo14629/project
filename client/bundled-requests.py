# Python program using the 'Requests' HTTP Request Python API.
# Also used the memory_profiler to profile the sendGetRequest function
#
# - Program uses BUNDLED HTTP REQUESTS and is sent to the proxy server
# - However, can also send individual files to the main server.
# - Cannot send non-bundled sequential requests to the main server - only single files
#
# Same tests as with the Java Programs

import requests
import time
import sys, getopt
import json
from memory_profiler import profile

URL = "http://172.20.10.2:"

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
        print "Last argument is the number of repeats (integer)"
        sys.exit(2)
    paths = paths[:-1]
    print paths
    url = createURL(paths, len(paths))
    sendGetRequest(url, repeats)

# Creating the bundled URL to be sent to the Proxy Server
# by using the correct parsing
def createURL(paths, total_paths):
    url = URL
    if total_paths == 1:
        url += "8081/"
    else:
        url += "8082/"
    for p in range(total_paths):
        extension = paths[p]
        extension += "*"
        url += extension
    url = url[:-1]
    return url

# send get requests to either the proxy or main server depending on input
@profile
def sendGetRequest(url, repeats):
    t_start = time.time()
    for j in range(repeats):
        response = requests.get(url)
        data = response.text
        print data
        print response.status_code
    t_end = time.time()
    print t_end-t_start
    try:
        decoded = json.loads(data)
        printLengths(decoded)
    except ValueError as v:
        print v, ". Assuming data is a string"
        print "data: ", len(data)

def printLengths(decoded):
    for key in decoded:
        value = decoded[key]
        print key, "length : ", len(value)

if __name__ == "__main__":
    main(sys.argv[1:])
