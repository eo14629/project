# Proxy server responsible for:
#   - Unpackaging bundled requests recieved from the client
#        and sending them to the server side
#   - Recieving the responses from the server and packaging
#        them as a JSON object then sending the object back
#        to the client.

import BaseHTTPServer
import requests
import json
import socket

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT_NUMBER = 8082
# Change SERVER_NAME depending on what the MAIN server address is.
SERVER_NAME = "http://172.20.10.2:8081/"

# Handles the Responses coming in from the Client
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        handleGet(s)

# split the path into different sections and direct to the
# bundled method, or single HTTP request method
def handleGet(s):
    extension = s.path.split('/')
    print "extension ", extension
    paths = extension[1].split('*')
    print paths
    if len(paths) > 1:
        response = bundle(paths)
        # print response
        s.wfile.write(response)
    else:
        response = singleGetRequest(paths[0])
        # print response
        s.wfile.write(response)

# a bundling method to send and receive multiple requests
# to the main server and then package them up as a JSON response to the Client.
def bundle(paths):
    response = {}
    for path in paths:
        response[path] = singleGetRequest(path)
    json_response = json.dumps(response)
    return json_response

# standard get request to the main server
# this will be used in the bundling method repeatedly
def singleGetRequest(path):
    url = SERVER_NAME + path
    server_response = requests.get(url)
    print path, " status_code: ", server_response.status_code
    return server_response.text

# set up the proxy server
def run():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), Handler)
    print "Proxy Server Starts\nURL: %s\nPort: %s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

# begin the program
run()
