package main
import (
	"fmt"
	"net"
	"log"
	"os"
	"time"
	"strconv"
)

func CheckErrors(err error) {
    if err  != nil {
        log.Println("Error : ", err)
		os.Exit(1)
    }
}

func main() {
	args := os.Args[1:]
	if len(args) != 3 {
		l := log.New(os.Stderr, "", 0)
		l.Println("Usage : client <host> <port> <number of packets>")
		os.Exit(1)
	}
	host := args[0]
	port := args[1]
	packetsNum, err := strconv.Atoi(args[2])
	CheckErrors(err)

	serverAddr, err:= net.ResolveUDPAddr("udp", fmt.Sprint(host + ":" + port))
	CheckErrors(err)
	localAddr, err := net.ResolveUDPAddr("udp", ":0")
	CheckErrors(err)

	conn, err := net.DialUDP("udp", localAddr,serverAddr)
	CheckErrors(err)
	defer conn.Close()	

	msg := "ping"
	buf := []byte(msg)
	var inBuf []byte
	for i:= 0; i < packetsNum; i++ {
		_, err = conn.Write(buf)
		CheckErrors(err)
		start := time.Now()
		conn.SetReadDeadline(start.Add(2 * time.Second))
		_, err = conn.Read(inBuf)
		if err != nil {
			log.Println("Timeout")
		} else {
			elapsed := time.Since(start)
			fmt.Printf("%3.4v\n", elapsed)
		}
	}
}