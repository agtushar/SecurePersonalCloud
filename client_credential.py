import socket                
import getpass

username=input('Username: ')
password=getpass.getpass('Password: ') 
confirm_password=getpass.getpass('Confirm Password: ') 
if password==confirm_password :
# Create a socket object 
	s = socket.socket()          
  
# Define the port on which you want to connect 
	port = 1243     
  
# connect to the server on local computer 
	s.connect(('127.0.0.1', port)) 
 
	output='signup'+'\n'+username+'\n'+password
# receive data from the server 
 
	s.sendall(output.encode('utf-8'))
	#c, addr = s.accept()
	print((s.recv(1024)).decode('utf-8'))
# close the connection 
	s.close() 

else :
	print('Sorry, Please try again')
