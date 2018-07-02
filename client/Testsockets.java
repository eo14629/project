import java.io.*;
import java.net.*;

class Testsockets {
  private String hostName = "172.20.10.2";
  private int portNumber = 8081;
  // private Socket echoSocket;
  // private PrintWriter out;
  // private BufferedReader in, stdIn;

  public static void main(String[] args) {
    Testsockets program = new Testsockets();
    program.connect();
  }

  // connects to a specific computer - should I instead connect to a more genric place -
  // try to mimic an app!
  private void connect() {
    try (
      Socket echoSocket = new Socket(hostName, portNumber);
      PrintWriter out = new PrintWriter(echoSocket.getOutputStream(), true);
      BufferedReader in = new BufferedReader(new InputStreamReader(echoSocket.getInputStream()));
      BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in))
    ) {
      String userInput;
      while ((userInput = stdIn.readLine()) != null) {
        out.println(userInput);
        System.out.println("echo: " + in.readLine());
      }
    } catch (UnknownHostException e) {
        System.err.println("Don't know about host " + hostName);
        System.exit(1);
    } catch (IOException e) {
        System.err.println("Couldn't get I/O for the connection to " + hostName);
        System.exit(1);
    }
  }
}
