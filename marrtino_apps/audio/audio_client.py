import sys
import socket
import time

ip = '127.0.0.1'
port = 9001

if (len(sys.argv)>1):
    ip = sys.argv[1]
if (len(sys.argv)>2):
    port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip,port))


sock.send('bip\n\r')
data = sock.recv(80)
print data

sock.send('TTS[it-IT] ciao, come stai?\n\r')
data = sock.recv(80)
print data

sock.send('TTS[en-US] very well, thank you!\n\r')
data = sock.recv(80)
print data


sock.send('TTS default language is english!\n\r')
data = sock.recv(80)
print data

sock.send('bop\n\r')
data = sock.recv(80)
print data

time.sleep(1)

sock.close()

