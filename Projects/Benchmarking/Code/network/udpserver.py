#!/usr/bin/env python

"""
A UDP server
"""

import socket
import time

#Aim         : To benchmark the network performance. 

#Description : This program is UDP Server program. 

#Contributor : Chaitanya Reddy Chatla (A203305053) 
#              Vivek Pabani (A20332117)


HOST="localhost"
PORT=5454

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind((HOST,PORT))

print "== UDP server started =="

for x in xrange(1000000):
    print s.recv(65536)

s.close()
