#connect to a minecraft server and cout works if the connection worked exit 0
#if the connection failed exit 1
#!/usr/bin/env python3
# Path: making a service\hello.py

import struct
import socket
import time
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json

host = "192.168.7.222"
port = 25565
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
#log into mincraft.net first

logindata = {'user': 'aaronsierra2nd@yahoo.com', 'password': 'M1crosoft002873', 'version': '1.8.9'}
data = urllib.urlencode(logindata)
print('attempting to log into mincraft.net')
req = urllib2.Request('https://login.minecraft.net/', data)
response = urllib2.urlopen(req)
returndata = response.read()
returndata = returndata.split(':')
mcsessionid = returndata[3]
del req
del returndata
print("session id: " + mcsessionid)
data = {'user':u'aaronsierra2nd@yahoo.com','host':u'192.168.7.222','port':u'25565','session':u'%s' % mcsessionid}

enc_user = data['user'].encode('utf-16BE')
stringfmt = u'%(user)s:%(hosts)s:%(port)d'
string = stringfmt % data
structfmt = '>bh'
packfmt = '>bih{}shiibBB'.format(len(enc_user))
packetbytes = struct.pack(packfmt,1,23,len(data['user']),enc_user,0,0,0,0,0)
s.send(packetbytes)
connhash = s.recv(1024)
print("conneciton hash: " + connhash)
print ("sending handshake")
req = urllib.urlopen('http://session.minecraft.net/game/joinserver.jsp?user=ElTragedyyy&sessionId=' + mcsessionid + '&serverId=' + connhash)
returndata = req.read()
if (returndata == 'OK'):
    print("connection successful")
    exit(0)  
else:
    print("connection failed")
    exit(1)