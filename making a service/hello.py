#connect to a minecraft server using sockets and python 3
import socket
import sys
import time
import urllib
import struct


HOST = "192.168.7.222"
PORT = "25565"
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#log into minecraft.net
loginInformation = {'user':'ElTragedyyy','password':'M1crosoft002873','version':'1.15.2'}
data = urllib.parse.urlencode(loginInformation)
print("attempting to log into minecraft.net")
#make a request to 'https://login.minecraft.net', send the data, and get the response
response = urllib.request.urlopen('https://login.minecraft.net', data.encode('utf-8'))
SiteResponse = response.read()
SiteResponse = SiteResponse.split(':')
mcsessionid = SiteResponse[2]
print("session id: " + mcsessionid)
data = {'user':'ElTragedyyy','host':u'127.0.0.1','port':25565}

stringfmt = u'%(user)s:%(host)s:%(port)s'
string = stringfmt % data
structfmt = '>bh'
packetbytes = struct.pack(structfmt, 2, len(string))+string.encode('utf-16be')
s.send(packetbytes)
connhash = s.recv(BUFFER_SIZE)
print("connection hash: " + connhash.decode('utf-16be'))
print("sending handshake")
if(SiteResponse == 'OK'):
    print("logged in, now sending data to server")
else:
    print("Oops, something went wrong")
time.sleep(5)

enc_user = data['user'].encode('utf-16be')
packfmt = '>bih{}shiibBB'.format(len(enc_user))
packetbytes = struct.pack(packfmt,1,23,len(data['user']), enc_user,0,0,0,0,0,0)
print(len(packetbytes))
print("sending " + packetbytes + ' to server')
s.send(packetbytes)

#if the server responds with a packet, print it and exit 0
#else print an error and exit 1
if(s.recv(BUFFER_SIZE)):
    print("received packet")
    sys.exit(0)
else:
    print("error")
    sys.exit(1)





