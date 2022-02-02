# Import socket module
from socket import * 
import sys # In order to terminate the program
from struct import *

# returns packetPhaseB1, udp_port, done repeating
def phaseBclient1SEND(packet, i):

    doneRepeat = False
    # packet = pack("!IHHIIHH", data_length, PCODE, ENTITY, repeat, udp_port, aLen, codeA)

    data_length, PCODE, ENTITY, repeat, udp_port, aLen, codeA = unpack("!IHHIIHH", packet)

    """
    struct

    data len 
    pcode = codeA
    entity = 1
    paketid = 0 -> repat -1
    data -> byte array

    """

    ENTITY = 1
    data  = bytearray(aLen)
    PCODEClientB = codeA
    packetId = i

    if (packetId == repeat - 1):
        doneRepeat = True

    while (len(data) % 4 != 0):
        data.append(0)

    data_length = len(data) + 4 + aLen



    packetBsending = pack("!IHHIs" , data_length, PCODE, ENTITY, packetId,data)

    return packetBsending, udp_port, doneRepeat, packetId

# return i
def phaseBclient1Rec(packet):

    # packetB1 = pack("!IHHI", data_length, PCODE, ENTITY, ak_packet_id)

    data_length, PCODE, ENTITY, ak_packet_id = unpack("!IHHI")
    print("Received acknowledgement packet from server: data_len:  {} pcode:  {} entity:  {} acknumber:  {}".format(data_length, ENTITY, ak_packet_id))

    return ak_packet_id



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
    pcode -> first phase == 0 (2 bytes)
    entity -> 2 bytes, (client uses 1 and server uses 2)
    data -> any siz % 4 == 0 (data must be padded until divisible by 4)

"""

# my additoin with the socket

#change socket to be padded to for but for right now this should work ??

x = 0
data_length = len(sentence)
# check if divisible by 4
if (data_length % 4 > 0):
    x = 1

while (len(sentence) % 4 !=  0):
    sentence += "0"

# after padding we can now send the data
sentenceStruct = pack('!IHH24s', len(sentence), PCODE, ENTITY, sentence.encode())

# phase A send
# -------------------------------------------------------------------------------------------
# phase B recive

#clientSocket.connect((serverName, serverPort))
clientSocket.sendto( sentenceStruct, (serverName, serverPort))

packetA, serverAddress = clientSocket.recvfrom(2048)

# creating new socket
clientSocket2 = socket(AF_INET, SOCK_DGRAM) 
i = 0

packetBsending, udp_port, doneRepeat, packetId = phaseBclient1SEND(packetA, i)

clientSocket2.sendto( packetBsending, (serverName, udp_port))

while not doneRepeat:

    packetB_rec = clientSocket2.recvfrom(2048)

    akc = phaseBclient1Rec(packetB_rec)

    if(ack == packetId):
        # send new packetID
        i += 1
        packetBsending, udp_port, doneRepeat, packetId = phaseBclient1SEND(packetA, i)
    else:
        packetBsending, udp_port, doneRepeat, packetId = phaseBclient1SEND(packetA, i)



# print('From server: ', modifiedSentence.decode())
clientSocket.close()

