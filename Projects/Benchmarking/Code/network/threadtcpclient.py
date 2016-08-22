#!/usr/bin/env python

from threading import Thread
import time
import sys
import socket

#Aim         : To benchmark the network performance. 

#Description : This program is TCP Client program. 

#Contributor : Chaitanya Reddy Chatla (A203305053) 
#              Vivek Pabani (A20332117)


clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def sendmsg(data):
	clientsocket.send(data)
	newdata = clientsocket.recv(65536)

def main():
    a=[]
    thr = []
    data = ""

    clientsocket.connect(('localhost',8000))

    for size in [1, 1024, 65536]:

        print "Size is %d" % size
		
        for x in range(0, size):
            a.append('b')
        data=''.join(a)
            
        for threads in xrange(1,3):

            #clientsocket.connect(('localhost',8000))
	            
            if threads == 1:

                t1 = Thread(target=sendmsg,args=(data,))
                tstart=time.clock()
                t1.start()	
                tend=((time.clock())-tstart)*1000
                
                print "Time for 1 thread is %f" % tend
                        
            elif threads == 2:

                if size == 1:
                   
                    t2 = Thread(target=sendmsg,args=(data,))
                    t3 = Thread(target=sendmsg,args=(data,))
                     
                    t2.daemon=True
                    t3.daemon=True

                    tstart=time.clock()

                    t2.start()
                    t3.start()

                    thr.append(t2)
                    thr.append(t3)

                elif size == 1024:
                    t4 = Thread(target=sendmsg,args=(data,))
                    t5 = Thread(target=sendmsg,args=(data,))
                        
                    t4.daemon=True
                    t5.daemon=True

                    tstart=time.clock()
                    
                    t4.start()
                    t5.start()

                    thr.append(t4)
                    thr.append(t5)

                elif size == 1024:
                    t6 = Thread(target=sendmsg,args=(data,))
                    t7 = Thread(target=sendmsg,args=(data,))
    
                    t6.daemon=True
                    t7.daemon=True
    
                    tstart=time.clock()
                            
                    t6.start()
                    t7.start()
    
                    thr.append(t6)
                    thr.append(t7)

                for t in thr:
                    while t.isAlive():
                        t.join(5)

                tend=(time.clock()-tstart)*1000
                print "Time for 2 threads is %f" % tend
                del thr[:]

            throughput =((65536*8)/(tend))/1000
	
            print "Throughput is %f" % throughput
            

    print "Main complete"
if __name__ == '__main__':
	main()

	
