import socket                

filename=input()
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 1272
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

temp='Download'+filename
s.sendall(temp.encode('utf-8'))

flag=0

data = (s.recv(1024))
if data==b'File not found':
	print(data)
else:
	wf=filename
	ch=b''
	with open(wf, 'wb') as f:
		print ('File opened')
		while True:
			print('Receiving data...')
			try:
   				cc=ch.decode('utf-8')
   				print(cc)
   				if cc=='File not found' :
   					data=data[:-14]
   					f.write(data)
   					break
			except UnicodeDecodeError:
				pass
			f.write(data)
			data = (s.recv(1024))
			ch=data[-14:]
			print(ch)
		flag=1
		f.close()

if flag==1 :
	print('Successfully downloaded')
s.close()
