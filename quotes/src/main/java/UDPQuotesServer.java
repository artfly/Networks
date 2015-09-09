import java.io.*;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

/**
 * Created by arty on 9/8/15.
 */
public class UDPQuotesServer {

    public static final String usage = "Usage : java UDPQuotesServer <port>";
    private static final int BUFSIZE = 1024;
    private static final String filename = "quotes";

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println(usage);
        }

        int localPort = Integer.parseInt(args[0]);
        BufferedReader br = null;

        try (DatagramSocket dSocket = new DatagramSocket(localPort)){
            byte[] receivedData = new byte[BUFSIZE];
            DatagramPacket dPacket = new DatagramPacket(receivedData, receivedData.length);
            try (InputStreamReader isr = new InputStreamReader((UDPQuotesServer.class.getResourceAsStream(filename)))) {
                br = new BufferedReader(isr);
                String line;
                while (true) {
                    dSocket.receive(dPacket);
                    InetAddress address = dPacket.getAddress();
                    int port = dPacket.getPort();

                    if ((line = br.readLine()) == null) {
                        break;
                    }
                    byte[] sendData = line.getBytes("UTF-8");

                    dPacket.setData(sendData);
                    dPacket.setLength(sendData.length);
                    dPacket.setAddress(address);
                    dPacket.setPort(port);
                    dSocket.send(dPacket);

                    System.out.println("Quote : " + line + " To : " + address + " " + port);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
