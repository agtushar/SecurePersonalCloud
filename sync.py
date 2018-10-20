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

temp='sync'
s.sendall(temp.encode('utf-8'))
s.recv(1024)
s.sendall(directory.encode('utf-8'))
s.recv(1024)
s.sendall(k.encode('utf-8'))
s.recv(1024)


for i in a:
	filename=directory+'/'+i
	print(filename)
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
	#print('End bit send')
	flag=0
	mess=(s.recv(1024)).decode('utf-8')
	print(mess)
	if mess=='File already synced' or mess=='File stored' :
		pass
	else :
		flag=1
		#print('Waiting for input')
		a=input()
		s.sendall(a.encode('utf-8'))
		if a=='N':
			wf=filename
			ch=b''
			with open(wf, 'wb') as f:
				#print ('File opened')
				data = (s.recv(1024))
				ch=data[-4:]
				#print(ch)
				while True:
					#print('Receiving data...')
					try:
		   				cc=ch.decode('utf-8')
		   				#print(cc)
		   				if cc=='done' :
		   					data=data[:-4]
		   					f.write(data)
		   					break
					except UnicodeDecodeError:
						pass
					f.write(data)
					data = (s.recv(1024))
					ch=data[-4:]
					#print(ch)
				flag=2
				f.close()
			print('File updated in client')
		

	if flag==1:
		#print('That extra message for overwriting')
		print((s.recv(1024)).decode('utf-8'))

	#print('This job is done')

print((s.recv(1024)).decode('utf-8'))
#s.send('Thank you for connecting')
dd=s.recv(1024).decode('utf-8')
if dd!='':
	print(dd)
# close the connection 
s.close() 
