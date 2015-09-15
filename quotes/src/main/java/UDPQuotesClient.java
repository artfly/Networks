import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

/**
 * Created by arty on 9/8/15.
 */
public class UDPQuotesClient {
    private final static int BUFSIZE = 1024;
    public final static String USAGE = "Usage : java UDPQuotesClient <hostname> <port>";

    public static void main(String[] args) {

        if (args.length < 2) {
            System.err.println(USAGE);
            return;
        }

        String host = args[0];
        int port = Integer.parseInt(args[1]);

        try (DatagramSocket dSocket = new DatagramSocket()) {
            InetAddress address = InetAddress.getByName(host);

            byte[] sendData = InetAddress.getLocalHost().toString().getBytes("UTF-8");

            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, address, port);
            dSocket.send(sendPacket);

            byte[] receiveData = new byte[BUFSIZE];
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
            dSocket.receive(receivePacket);

            String quote = new String(receiveData, 0, receivePacket.getLength(), "UTF-8");
            System.out.println(quote);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
