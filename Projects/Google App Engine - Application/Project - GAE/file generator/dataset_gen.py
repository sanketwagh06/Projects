import random

#Program to create number of files of particular size

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

x = input("\n Enter the number of files to be generated\n")
y = input("\n Enter the size in KB of file to be generated\n")

for count in xrange(int(x)): 
    fname = str(count)+'.txt'
    file = open(fname,"ab")
    size = int(y) 
    
    for sizeln in xrange(size*10):
        file.write(''.join(random.choice(chars) for i in xrange(99)) +"\n")
    file.close()
