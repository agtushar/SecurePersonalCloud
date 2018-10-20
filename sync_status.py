import socket                
import os

directory=input()
a=os.listdir(directory)
#print(a)
k=str(len(a))
#print(k)
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 1273
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

temp='synstatus'
s.sendall(temp.encode('utf-8'))
s.recv(1024)
s.sendall(directory.encode('utf-8'))
s.recv(1024)
s.sendall(k.encode('utf-8'))
s.recv(1024)


for i in a:
	filename=directory+'/'+i
	#print(filename)
	s.sendall(filename.encode('utf-8'))
	s.recv(1024)
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		s.send(l)
		#print('Sending ... ')
		#print(l)
		l = f.read(1024)
	f.close()

	#print('Done sending')
	s.send(b'over')
	s.recv(1024)
	#print('Next')
	#print('End bit send')

print((s.recv(1024)).decode('utf-8'))
print((s.recv(1024)).decode('utf-8'))
print((s.recv(1024)).decode('utf-8'))
print((s.recv(1024)).decode('utf-8'))
#s.send('Thank you for connecting')
# close the connection 
s.close() 
