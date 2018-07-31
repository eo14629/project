// Minimal server: log request details
var HTTP = require('http');
var fs = require("fs");
var ip = require("ip");

start(8081);

// Provide a service to localhost only.
function start(port) {
   var service = HTTP.createServer(handle);
   service.listen(port,'0.0.0.0');
   console.log("URL:" + ip.address() + "\nPort:" + port);
}

// Deal with a request.
function handle(request, response) {
   printRequest(request);
   var url = request.url.toLowerCase();
   if (checkURL(url)) return fail(response, 500, "ERROR: INVALID URL");
   direct(url, request, response);
}

function printRequest(request) {
  let body = [];
  console.log("Method:", request.method);
  console.log("URL:", request.url);
  console.log("Headers:", request.headers);
  request.on('data', (chunk) => {
    body.push(chunk);
  }).on('end', () => {
    body = Buffer.concat(body).toString();
    // console.log("Body:", body);
  });
}

// make sure that the URL is not suspect
function checkURL(url) {
   if(url.includes("./") ||
   url.includes("//") ||
   url.includes("/.") ||
   url.includes("%20")) {
      console.log("Dangerous URL entered" + url);
      return true;
   }
   return false;
}

// after the URL has been checked, direct user to the post function
// or the get function for further directioning.
function direct(url, request, response) {
  var extension;
  if (url.startsWith("/get-")) {
    extension = url.split("-")[1];
    get(extension, request, response);
  } else if (url.startsWith("/post-")) {
    extension = url.split("-")[1];
    post(extension, request, response);
  } else {
    reply(404, response, 'text/plain' , "404 Page not found");
  }
}

// function to deal with HTTP GET Requests
function get(extension, request, response) {
  if (extension == "good") {
    reply(200, response, 'text/html' , "good");
  } else if (extension.startsWith("file")) {
    var file = "./txt" + extension.split("file")[1] + ".txt"
    fs.readFile(file, ready);
    function ready(err, content) {
      if (err) {reply(400, response, 'text/plain' , "400 - File '"+ file + "' does not exist in server library")}
      else {reply(200, response, 'application/octet-stream' , content);}
    }
  } else if (extension == "") {
    reply(200, response, 'text/plain' , "OK");
  } else {
    reply(404, response, 'text/plain' , "404 - Page not found");
  }
}

// function to deal with HTTP POST Requests
function post(extension, request, response) {
  console.log("extension = " + extension);
  if (extension == "") {
    reply(200, response, 'text/plain' , "post OK");
  } else {
    reply(404, response, 'text/plain' , "404 - Page not found");
  }
}

// Send a reply of any type and status
function reply(status_code, response, type, content) {
   var headers = { 'content-type': type };
   // console.log("Response: " + content);
   console.log("STATUS CODE sent: " + status_code);
   response.writeHead(status_code, headers);
   response.write(content)
   response.end();
}
