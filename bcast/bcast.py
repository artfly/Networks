import socket
import time
import sys


def main():
    if len(sys.argv) != 2:
        print("usage : %s port")
        sys.exit()
    port = int(sys.argv[1])
    count = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(2)
    sock.bind(('', port))

    sock.sendto(bytes("IBORN", "utf-8"), ('255.255.255.255', port))
    lifetime = time.time() + 10
    while time.time() < lifetime:
        try:
            message, address = sock.recvfrom(1024)
            message = message.decode("utf-8")
            print("Message : %s from : %s" % (message, str(address)))
            if message == "IBORN":
                sock.sendto(bytes("ILIVE", "utf-8"), address)
                print(address)
                me = (socket.gethostbyname(socket.gethostname()), sock.getsockname()[1])
                if address != me:
                    count += 1
                print("Current count of copies : %s" % count)
            elif message == "ILIVE":
                if address != me:
                    count += 1
                print("Current count of copies : %s" % count)
            elif message == "IEXIT":
                if address != me:
                    count -= 1
                print("Current count of copies : %s" % count)
        except socket.timeout:
            print("No new messages in 2 seconds.")
    time.sleep(1)
    sock.sendto(bytes("IEXIT", "utf-8"), ('255.255.255.255', port))
    print("Count at exit : %s" % count)


if __name__ == "__main__":
    main()
