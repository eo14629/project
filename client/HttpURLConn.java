// Using the HttpURLConn Java class to produce HTTP Gets and Posts

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.time.*;

import java.net.*;
import java.net.HttpURLConnection;

class HttpURLConn {
  private String urlName = "http://192.168.0.34:8081/";
  private DataOutputStream out;
  private BufferedReader in, stdIn;

  public static void main(String[] args) {
    HttpURLConn program = new HttpURLConn();
    program.appendURL();
  }

  // waiting function - gets URL from user.
  private void appendURL() {
    stdIn = new BufferedReader(new InputStreamReader(System.in));
    String userInput;
    try {
      while ((userInput = stdIn.readLine()) != null) {
        if (userInput.startsWith("get-")) {
          Instant t1, t2;
          t1 = Instant.now();
          // loop round this line:
          for (int i=0; i<8000; i++) {
            get(userInput);
          }
          t2 = Instant.now();
          printDuration(Duration.between(t1, t2).toMillis());
        } else if (userInput.startsWith("post-")){
          Path file = FileSystems.getDefault().getPath("./txt300.txt");
          byte[] fileArray = Files.readAllBytes(file);
          Instant t1, t2;
          t1 = Instant.now();
          // loop round this line:
          for (int i=0; i<10000; i++) {
            post(userInput, fileArray);
          }
          t2 = Instant.now();
          printDuration(Duration.between(t1, t2).toMillis());
        } else {
          System.err.println("Incorrect url format: must start with 'get-' or 'post-'");
        }
      }
    } catch(IOException d) {
      System.err.println("d: " + d.getMessage());
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
    } catch (IOException getFail) {
      System.err.println("getFail: " + getFail.getMessage());
    }
  }

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
    // for (int i=0; i<conn.getHeaderFields().size(); i++) {
    //   System.out.println("Header Name - " + conn.getHeaderFieldKey(i) + ", Value - " + conn.getHeaderField(i));
    // }
    // // System.out.println("Property size: " + conn.getRequestProperties().size());
    // for (String propertyKey : conn.getRequestProperties().keySet()) {
    //   System.out.println("Property name - " + conn.getRequestProperty(propertyKey));
    // }
  }
}
