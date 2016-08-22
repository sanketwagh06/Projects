#!/bin/bash

echo "==Shell script to run network benchmark code=="

echo "Starting UDP server"

./udpserver.py > udp.outerr 2>&1 &
echo $? "is UDP server exit code"

echo "Starting UDP client"
./udpclient.py

echo "Starting TCP server"

./tcpserver.py > tcp.outerr 2>&1 &
echo $? "is TCP server exit code"

echo "Starting TCP client"
./threadtcpclient.py

