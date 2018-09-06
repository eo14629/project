SERVER-SIDE

programs:
    main-server.js
    proxy.py

server-side data:
    *.txt files.

Servers will not work on eduroam WiFi

Start main nodeJS server by just running the program with node and the node modules
given by the package-lock.json file. Port 8081 is used.

The proxy server can be run by entering the IP address and port number of the
main server on line 16 of the proxy.py file. port 8082 is used for the proxy server

CLIENT-SIDE

programs:
    c_example.c
    HttpURLConn.java
    sequential-request.py
    bundled-requests.py

client-side data:
    *.txt files

Ensure that the correct main server IP address and port numbers are entered into the
correct variable names on the client-side programs.

It is assumed on the bundled-requests.py file that the proxy is on the Same
computer as the main server.

The usage of the client side files will display if the programs are run.

Simple request response information will be accumulated by these files. These programs
have been designed to serve a purpose: to measure the energy related to downloading and uploading
files through HTTP requests by the use of an external ammeter.
