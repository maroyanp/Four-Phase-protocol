# Import socket module
from socket import * 
import sys # In order to terminate the program
from struct import *
import time

serverName = 'localhost'
#serverName = '10.84.88.53'
# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sentence = input(' Input lower case sentence: ')
ENTITY = 1
PCODE = 0


# phase A send
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

while (len(sentence) % 4 !=  0):
    sentence += "0"

# after padding we can now send the data
packetSendA1 = pack('!IHH24s', len(sentence), PCODE, ENTITY, sentence.encode())

# -------------------------------------------------------------------------------------------
# Phase A rec

#clientSocket.connect((serverName, serverPort))
clientSocket.sendto( packetSendA1, (serverName, serverPort))

packetA_Rec, serverAddress = clientSocket.recvfrom(2048)

# clientSocket.close()

# -------------------------------------------------------------------------------------------
# Phase B-1 send

# creating new socket
clientSocket2 = socket(AF_INET, SOCK_DGRAM) 

data_length, PCODE, ENTITY, repeat, udp_port, aLen, codeA = unpack("!IHHIIHH", packetA_Rec)

doneRepeat = False
ENTITY = 1
data  = bytearray(aLen)
PCODE = codeA
packetId = 0

if (packetId == repeat - 1):
    doneRepeat = True

data_length = len(data) + 4 + aLen

while (data_length % 4 != 0):
    data.append(0)
    data_length = len(data) + 4 + aLen


# print("len of data ", data_length)


# now we continue to send till acknowlegment

# now we send and wait for a recive

while (packetId < repeat):
    packetBsending = pack("!IHHIs" , data_length, PCODE, ENTITY, packetId,data)
    clientSocket2.sendto(packetBsending, (serverName, udp_port))
    
    try:
        p_clinet_r_B1, serverAddress = clientSocket2.recvfrom(2048)
        data_length, PCODE, ENTITY, ak_packet_id = unpack('!IHHI',p_clinet_r_B1)
        print("Received acknowledgement packet from server: data_len: {} pcode: {} entity: {} acknumber: {}".format(
            data_length, PCODE, ENTITY, ak_packet_id))
        packetId += 1
    
    except:
        time.sleep(5)
        continue #after 5 seconds?

# now recive from B2
p_clinet_r_B2, serverAddress = clientSocket2.recvfrom(2048)


data_length3, PCODE, ENTITY3, tcp_port, codeB =  unpack("!IHHII", p_clinet_r_B2)
print("Received final packet: data_len:  {} pcode:  {} entity: {}  tcp_port: {}  codeB: {}".format(
    data_length3, PCODE, ENTITY, tcp_port, codeB))
print("------------ End of Stage B  ------------\n")
# ------------------------------------------------------------------------------------------------------------
print("------------ Starting Stage C  ------------")

c_tcpSocket = socket(AF_INET, SOCK_STREAM)
print("connecting to server at tcp port {}".format(tcp_port))
c_tcpSocket.connect((serverName, tcp_port))
time.sleep(5)
p_client_r_C1 = c_tcpSocket.recv(1024)

data_lengthC1, PCODE, ENTITY, repeat2, len2, codeC, Rchar = unpack("!IHHIIIc",p_client_r_C1)
Rchar = Rchar.decode()

print(f"Received packet from server: data_len: {data_lengthC1}  pcode: {PCODE} " 
    +f"entity: {ENTITY} repeat2: {repeat2}   len2: {len2}   codeC: {codeC}   char:  {Rchar}")
print("------------ End of Stage C  ------------\n")