# Secure Personal Cloud
course project for CS251, IIT Bombay, autumn 2018. Developed by team 011bytes.
Motivation is to prevent cloud leaks .The client encrypts each file before uploading to the cloud server with a key known to only user(not stored on server) and decrypts before downloading so that the information is not exposed even if the server is hacked.

## Getting Started
Clone our repo
```
git clone https://github.com/tusharag121099/SecurePersonalCloud
```
### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing and Signup


run install.sh in command line
```
sudo bash install.sh
```
Signup with your name on browser
```
http://127.0.0.1:8000/accounts/signup/
```
## Linux Client 


### configure user

```
spc configure
```


### configure directory 

```
spc observe <directory name>
```
give absolute path in directory name


### configure encryption scheme

We offer 3 encryption schemes on linux client:
* [ARC4](https://en.wikipedia.org/wiki/RC4): requires one key of length 8 
* [DES](https://en.wikipedia.org/wiki/Data_Encryption_Standard): requires one key of length 8 
* [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard): requires two keys of length 16 each 

```
spc en-de update
```
enter scheme with which you would like to encrypt your data and a key

### Upload/Download

```
spc sync
```
This makes client's observed directory and server's copy(encryted though) to be exact same snapshots of each other.
If a file is available on server but not on client, there are two options either to delete server's copy or to download server's copy.
Conversly, if a files is available only on client, this command uploads encryted file(s) to server.

### Versioning

```
spc version
```

### Update
 ```
 spc update
 ```
## Web Client

### Signup/Login


First run local server * [https:/127.0.0.1/](https:/127.0.0.1/) and then
Login * [https:/127.0.0.1/accounts/login](https:/127.0.0.1/accounts/login) or
Signup * [https:/127.0.0.1/accounts/signup](https:/127.0.0.1/accounts/signup) and then login.
A user has to be logged in for web client.


### Decryption

Enter Decryption key and encryption schema.
* [https:/127.0.0.1/storage/keyVerify](https:/127.0.0.1/storage/keyVerify)
Enter decryption key at key1 for ARC4 and DES.


### Files

Find files at * [http://127.0.0.1:8000/storage/direct_Str](http://127.0.0.1:8000/storage/direct_Str)

## Team 011bytes

* [Tushar Agrawal](https://github.com/tusharag121099)
* [Arnab Jana](https://github.com/Arnabjana1999)
* [Mohan Abhyas](https://github.com/MohanAbhyas)
