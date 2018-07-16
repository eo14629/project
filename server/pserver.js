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
    fof(response);
  }
}

// function to deal with HTTP GET Requests
function get(extension, request, response) {
  if (extension == "good") {
    reply(response, 'text/html' , "good");
  } else if (extension == "file") {
    fs.readFile('./txt1.txt', ready);
    function ready(err, content) {
      reply(response, 'application/octet-stream' , content);
    }
  } else if (extension == "") {
    reply(response, 'text/plain' , "OK");
  } else {
    fof(response);
  }
}

// function to deal with HTTP POST Requests
function post(extension, request, response) {
  console.log("extension = " + extension);
  if (extension == "") {
    reply(response, 'text/plain' , "post OK");
  } else {
    fof(response);
  }
}

// 404 not found
function fof(response) {
  reply(response, 'text/plain' , "404 Page not found");
}

// Send a reply of any type
function reply(response, type, content) {
   var headers = { 'content-type': type };
   // console.log("Response: " + content);
   response.writeHead(200, headers);
   response.write(content)
   response.end();
}
