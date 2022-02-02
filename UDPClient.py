# Import socket module
from ast import While
from socket import * 
import sys # In order to terminate the program
import struct
import time

serverName = 'localhost'
#serverName = '10.84.88.53'
# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
print("-------------- Starting Stage A -------------")
sentence = input('Input correct message (CASE SENSITIVE): ')
pCode = 0
ENTITY = 1
#may have to switch to bytes

while ((len(sentence) % 4) > 0):
    sentence += "0"

dLength = len(sentence)
sentenceStruct = struct.pack('!IHH24s',dLength,pCode,ENTITY,sentence.encode())

clientSocket. sendto( sentenceStruct, (serverName, serverPort))

phaseASStruct, serverAddress = clientSocket.recvfrom(2048)
dLength2, pCode2, ENTITY2, repeat, udp_port, len, codeA = struct.unpack('!IHHIIHH', phaseASStruct)
print("Received Packet from server: data_len: {} pcode: {} entity: {} repeat: {} len: {} udp_port: {} codeA: {}".format(dLength2,pCode2,ENTITY2,repeat,len,udp_port,codeA))
print("------------ End of Stage A ---------------")
print()
print("------------ Starting Stage B -------------")

pCode = codeA
packet_id = 0
data = bytearray(len)
dLength = len + 4 
count = 0
while (dLength % 4 > 0):
    data.append(0)
    dLength += 1

clientSocket.connect((serverName, udp_port))

while(packet_id < repeat - 1):

    phaseBCStruct = struct.pack('!IHHIs', dLength, pCode, ENTITY, packet_id, data)
    clientSocket.sendto(phaseBCStruct,(serverName, udp_port))
    #somehow wait to receive ack packet
    #need retransmission interval of 5 seconds
    try:
        ackStruct, serverAddress = clientSocket.recvfrom(2048)
        dLength2, pCode, ENTITY2, acked_packet_id = struct.unpack('!IHHI',ackStruct)
        print("Received acknowledgement packet from server: data_len: {} pcode: {} entity: {} acknumber: {}")
        packet_id = acked_packet_id
    
    except:
        time.sleep(5)
        continue #after 5 seconds?

        
    
   


#print('From server: ', phaseAC.decode())
clientSocket.close()

