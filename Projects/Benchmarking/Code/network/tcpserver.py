#!/usr/bin/env python

import socket
import time
import sys



#Aim         : To benchmark the network performance. 

#Description : This program is TCP Server program. 

#Contributor : Chaitanya Reddy Chatla (A203305053) 
#              Vivek Pabani (A20332117)



"""
TCP Server
"""

# Create Connection 
serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind(('localhost',8000))
serversocket.listen(1)
clientsocket,clientaddr=serversocket.accept()
print 'connection from',clientaddr

# Data exchange
while True:

    data=clientsocket.recv(65536)
    
    if not data:
        break

    clientsocket.send(data)

#    serversocket.shutdown(1)

