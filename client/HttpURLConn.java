// Using the HttpURLConn Java class to produce HTTP GETS and POSTS

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.time.*;

import java.net.*;
import java.net.HttpURLConnection;

class HttpURLConn {
  private String urlName = "http://172.20.10.2:8081/";
  private DataOutputStream out;
  private BufferedReader in, stdIn;

  public static void main(String[] args) {
    HttpURLConn program = new HttpURLConn();
    if (program.checkArgs(args)) {
        program.direct(args);
    } else {
        System.err.println("Usage: java HttpURLConn -request(e.g get-file1000) num_repeats");
    }
  }

  // make sure the arguments are of the correct format
  private boolean checkArgs(String[] args) {
      boolean ret_val = false;
      if  (args.length==2 &&
          (args[0].startsWith("get-") || args[0].startsWith("post-"))) {
          try {
              int repeats = Integer.parseInt(args[1]);
              if (args[0].startsWith("post-")) {
                  try {
                      int extension = Integer.parseInt(args[0].split("post-file")[1]);
                      ret_val = true;
                  } catch(Exception d) {}
              } else {
                  ret_val = true;
              }
          } catch(Exception e) {}
      }
      return ret_val;
  }

  // directs program to carry out a POST or GET request.
  private void direct(String[] args) {
    String request = args[0];
    int repeats = Integer.parseInt(args[1]);
    if (request.startsWith("get-")) {
      Instant t1, t2;
      t1 = Instant.now();
      // loop round this line:
      for (int i=0; i<repeats; i++) {
        get(request);
      }
      t2 = Instant.now();
      // printDuration(Duration.between(t1, t2).toMillis());
    } else {
      int extension = Integer.parseInt(args[0].split("post-file")[1]);
      Path file = FileSystems.getDefault().getPath("./txt" + extension + ".txt");
      try {
          byte[] fileArray = Files.readAllBytes(file);
          Instant t1, t2;
          t1 = Instant.now();
          // loop round this line:
          for (int i=0; i<repeats; i++) {
            post(request, fileArray);
          }
          t2 = Instant.now();
          printDuration(Duration.between(t1, t2).toMillis());
      } catch(IOException e) {
          System.err.println(e.getMessage());
      }
    }
  }

  private void printDuration(double millis) {
	  for (int j=0; j<40; j++) {
		for (int k=0; k<j; k++) {
			System.out.print(millis/1000 + "s");
		}
		System.out.println("...");
	  }
  }

  // The get request - makes a connection to the server
  // and reads in the recieved input.
  // now not going to print the response as this should Not
  //    be involved in the energy calculations
  private void get(String userInput) {
	String response;
    try {
      URL url = new URL(urlName + userInput);
      HttpURLConnection conn = (HttpURLConnection) url.openConnection();
      conn.setRequestMethod("GET");
      // printRequest(conn);
      InputStreamReader stream = new InputStreamReader(conn.getInputStream());
      in = new BufferedReader(stream);
      response  = "echo: " + in.readLine();
      in.close();
      System.out.println("Response: " + response);
    } catch (IOException getFail) {
      System.err.println("getFail: " + getFail.getMessage());
    }
  }

  // same as get() but for posts.
  private void post(String userInput, byte[] file) {
	String response;
    try {
      URL url = new URL(urlName + userInput);
      HttpURLConnection conn = (HttpURLConnection) url.openConnection();
      conn.setRequestMethod("POST");
      conn.setDoOutput(true);
      // printRequest(conn);
      try( DataOutputStream wr = new DataOutputStream(conn.getOutputStream())) {
        wr.write(file);
      } catch (IOException OutputStreamFail) {
		System.err.println("OutputStreamFail: " + OutputStreamFail.getMessage());
	  }
      InputStreamReader stream = new InputStreamReader(conn.getInputStream());
      in = new BufferedReader(stream);
      response  = "echo: " + in.readLine();
      in.close();
    } catch (IOException postFail) {
	  System.err.println("postFail: " + postFail.getMessage());
    }
  }

  // printing all parts of the HTTP Request
  private void printRequest(HttpURLConnection conn) {
    System.out.println("HTTP REQUEST:");
    System.out.println(conn.getRequestMethod());
    for (int i=0; i<conn.getHeaderFields().size(); i++) {
      System.out.println("Header Name - " + conn.getHeaderFieldKey(i) + ", Value - " + conn.getHeaderField(i));
    }
    // System.out.println("Property size: " + conn.getRequestProperties().size());
    for (String propertyKey : conn.getRequestProperties().keySet()) {
      System.out.println("Property name - " + conn.getRequestProperty(propertyKey));
    }
  }
}
