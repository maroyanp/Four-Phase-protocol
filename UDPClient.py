# Import socket module
from socket import * 
import sys # In order to terminate the program
from struct import *


serverName = 'localhost'
#serverName = '10.84.88.53'
# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sentence = input(' Input lower case sentence: ')
ENTITY = 1
PCODE = 0

# -------------------------------------------------------------------------------------------
"""
struct: 
    
    data_length --> 4 bytes (length of packet)
    pcode -> first phase == 0
    entity -> 2 bytes, (client uses 1 and server uses 2)
    data -> any siz % 4 == 0 (data must be padded until divisible by 4)

"""

# my additoin with the socket

#change socket to be padded to for but for right now this should work ??

x = 0
# check if divisible by 4
if (len(sentence) % 4 > 0):
    x = 1

while x:
    sentence += "0"
    if (len(sentence) % 4 > 0):
        x = 1
    else:
        x = 0

# after padding we can now send the data
sentenceStruct = pack('!IIH20s', len(sentence), PCODE, ENTITY, sentence.encode())


# -------------------------------------------------------------------------------------------

#clientSocket.connect((serverName, serverPort))
clientSocket.sendto( sentenceStruct, (serverName, serverPort))
modifiedSentence, serverAddress = clientSocket.recvfrom(2048)

print('From server: ', modifiedSentence.decode())
clientSocket.close()

