import BaseHTTPServer
import requests
import json
import socket
import time

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT_NUMBER = 8082
SERVER_NAME = "http://192.168.0.34:8081/"

# Handles the Responses coming in from the Client
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("path accessed: %s\n" % s.path)

        # split the path into different sections
        extension = s.path.split('/')
        paths = extension[1].split('&')
        print paths
        if len(paths) > 1:
            response = bundle(paths)
            print response
            s.wfile.write(response)
        else:
            response = getRequest(paths[0])
            print response
            s.wfile.write(response)

# a bundling method to send and receive multiple requests
# to the main server and then package them up as a JSON response.
def bundle(paths):
    response = {}
    for path in paths:
        response[path] = getRequest(path)
    json_response = json.dumps(response)
    return json_response

# standard get request to the main server
# this will be used in the bundling method repeatedly
def getRequest(path):
    url = SERVER_NAME + path
    server_response = requests.get(url)
    return server_response.text

# set up the proxy server
def run():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), Handler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

run()
