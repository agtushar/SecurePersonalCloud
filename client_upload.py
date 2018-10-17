import socket                

filename=input()
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 1272
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

temp='Upload'+filename
s.sendall(temp.encode('utf-8'))
s.recv(1024)
f = open(filename,'rb')
l = f.read(1024)
while (l):
	s.send(l)
	print('Sending ... ')
	print(l)
	l = f.read(1024)
f.close()

print('Done sending')
s.send(b'over')
print('End bit send')
flag=0
mess=(s.recv(1024)).decode('utf-8')
print(mess)
if mess=='file exists. Do you want to overwrite?' :
	flag=1;
	#print('correct')
	a=input()
	s.sendall(a.encode('utf-8'))

if flag==1:
	print((s.recv(1024)).decode('utf-8'))

#s.send('Thank you for connecting')

# close the connection 
s.close() 
