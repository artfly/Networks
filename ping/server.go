package main
import (
	"fmt"
	"net"
	"log"
	"os"
)

const BUFSIZE = 1024

func checkErrors (err error) {
	if err != nil {
		log.Println("Error : ", err)
		os.Exit(1)
	}
}

func main() {
	args := os.Args[1:]
	if len(args) != 1 {
		l := log.New(os.Stderr, "", 0)
		l.Println("Usage : server <port>")
		os.Exit(1)
	}
	
	serverAddr, err := net.ResolveUDPAddr("udp", fmt.Sprint(":" + args[0]))
	checkErrors(err)
	serverConn, err := net.ListenUDP("udp", serverAddr)				
	checkErrors(err)
	defer serverConn.Close()

	buf := make([]byte, BUFSIZE)
	msg := "pong"
	outBuf := []byte(msg)
	for {
		n, addr, err := serverConn.ReadFromUDP(buf)
		checkErrors(err)
		fmt.Println("Received : ", string(buf[0:n]), " from : ", addr)
		_, err = serverConn.WriteToUDP(outBuf, addr)
		checkErrors(err)
	}
}