import socket
import sqlite3
conn=sqlite3.connect("db.sqlite3") 
cur=conn.cursor()

s = socket.socket()          
print ("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 1272     
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print ("socket binded to %s" %(port)) 
  
# put the socket into listening mode 
s.listen(5)      
print ("socket is listening")            
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print ('Got connection from', addr) 
   st=""
  # while True:
   print('receiving data...')
   m=(c.recv(1024)).decode('utf-8')
   print(m)
   st=st+m
   	#print('data=%s', (m))
   	#if m=='****':
   	#	break
   
   data = m.split('\n') #split string into a list
   #print(st[0:6])
   string=''
   #print(st)
   if st[0:6]=='Upload' :
   	nm=st[6:]
   	flag=1
   	print('Done')
   	c.send(b'Start')
   	info=b''
   	data=b''
   	ch=b''
   	while True:
   		print('receiving data...')
   		print('boy')
   		try:
   			cc=ch.decode('utf-8')
   			print(cc)
   			if cc=='over' :
   				break
   		except UnicodeDecodeError:
   			pass
   		print(flag)
   		print('animal')
   		data=c.recv(1024)
   		print('women')
   		ch=data[-4:] 
   		print(ch)
   		info=info+data
   	info=info[:-4]
   	print('here')
   	cur.execute('SELECT id, filename FROM Files')
   	name=cur.fetchall()
   	print('here1')
   	for row in name:
   		if row[1]==nm :
   			c.send(b'file exists. Do you want to overwrite?')
   			m=(c.recv(1024)).decode('utf-8')
   			if m=='Y' :
   				flag=2
   				cur.execute("DELETE FROM Files WHERE filename = ?", (nm,))
   			if m=='N' :
   				flag=0
   				c.send(b'No changes')
   			break
   	print('here2')
   	print(flag)
   	if flag==1 or flag==2 :
   		print(m)
   		cur.execute('Insert into Files(filename,document) values(?,?)',(nm,info))
   		conn.commit()
   		if flag==1 :
   			c.send(b'File stored')
   		if flag==2 :
   			c.send(b'File overwritten') 
   	#print('committed')
   		#cur.close()
   		#conn.close()
   	#c.send(b'File stored')	
   	#c.send(b'Sorry, Username already exists')		
   # send a thank you message to the client. 
   #s.connect((addr[0], addr[1]))
   # Close the connection with the client 
   	c.close() 
   print(st[0:8])
   if st[0:8] == 'Download':
   	flag=0
   	nm=st[8:]
   	cur.execute('SELECT * FROM Files')
   	name=cur.fetchall()
   	print('step1')
   	for row in name:
   		if(row[2]==nm):
   			print('BIG')
   			#print(row[1])
   			print('Here')
   			l=(row[1])[0:1024]
   			print(l)
   			ctr=1024
   			print(ctr)
   			while l:
   				c.send(l)
   				l=(row[1])[ctr:ctr+1024]
   				print(l)
   				ctr=ctr+1024
   				print(ctr)
   			break
   			c.send(b'done')
   			flag=1
   	print('Yes')
   	if flag==0:
   		c.sendall(b'File not found')


   if data[0]=='signup':
   	cur.execute('SELECT * FROM Credential')
   	name=cur.fetchall()
   	idd=1
   	for row in name:
   		if row[1]==data[1]:
   			idd=-1
   	if idd==1:
   		cur.execute('Insert into Credential(name,password) values(?,?)',(data[1],data[2]))
   		conn.commit()
   		#cur.close()
   		#conn.close()
   		c.send(b'Successfully added')
   	else:
   		c.send(b'Sorry, Username already exists')		
   # send a thank you message to the client. 
   #s.connect((addr[0], addr[1]))
   # Close the connection with the client 
   	c.close() 

   if data[0]=='login':
   	user=data[1]
   	cur.execute('SELECT * FROM Credential')
   	name=cur.fetchall()
   	idd=-1
   	for row in name:
   		if row[1]==data[1] and row[2]==data[2]:
   			idd=row[0]
   # send a thank you message to the client.
   	if idd==-1: 
   #s.connect((addr[0], addr[1]))
   		c.send(b'Wrong Credentials')
   	else:
   		c.send(b'You are logged in')

   
   # Close the connection with the client 
   	c.close()
