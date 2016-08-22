#!/usr/bin/env python

"""
A UDP client
"""

from threading import Thread
import socket
import time
import sys

#Aim         : To benchmark the network performance. 

#Description : This program is UDP Client program. 

#Contributor : Chaitanya Reddy Chatla (A203305053) 
#              Vivek Pabani (A20332117)


clientsocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def sendmsg(data):
	clientsocket.send(data)

def main():
        print "== UDP Client =="
	clientsocket.connect(('localhost',5454))
	a = []
	thr = []
        
	for size in [988,8000]: # Max message size possible with UDP is 8000
		for x in xrange(1,size):
			a.append('=')
		data=''.join(a)
                
        for threads in [1,2]:	
            if threads == 2:
                print "Using two threads ..."
	        t1 = Thread(target=sendmsg,args=(data,))
	        t2 = Thread(target=sendmsg,args=(data,))
	        t1.daemon=True
	        t2.daemon=True
	        tstart=time.clock()
	        t1.start()
	        t2.start()
	        thr.append(t1)
	        thr.append(t2)
	        for t in thr:
	        	while t.isAlive():
	        		t.join(5) 
	        tend=(time.clock()-tstart)*1000
	    	print "Time elapsed is %f" % tend
                throughput =((sys.getsizeof(data)*8)/(1024*tend))*1000
                print "Throughput is %f" % throughput
	    
            if threads == 1:
                print "Using one thread ..."
	    	t3 = Thread(target=sendmsg,args=(data,))
	    	tstart=time.clock()
	    	t3.start()	
	    	tend = (time.clock()-tstart)*1000
	    	print "Time elapsed is %f" % tend
                throughput =((sys.getsizeof(data)*8)/(1024*tend))
                print "Throughput is %f" % throughput

	print "Main complete"
	exit(0)

if __name__ == '__main__':
	main()

