# Import socket module
from socket import *
import struct 
import sys # In order to terminate the program
from struct import *
from random import *

# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

print('The server is ready to receive')
print("-------------Starting Stage A --------------")
print()
#serverSocket.settimeout(100)

sentenceStruct, clientAddress = serverSocket.recvfrom(1024)
dLength, pCode, ENTITY, data = struct.unpack('!IHH24s', sentenceStruct)
decodeSentence = data.decode()
print("receiving from the client: data_len: {} pcode: {} entity: {} data: {}".format(dLength, pCode, ENTITY, data))

if (dLength % 4 != 0):
	print("Incorect data length CLOSING CONNECTION")
	serverSocket.close()
		
#decodeSentence = str(decodeSentence).replace('0', "")
if(str(decodeSentence) == "Hello World!!!"):
	print("Incorect data CLOSING CONNECTION")
	serverSocket.close()
		
if(pCode != 0 or ENTITY != 1):
	print("incorect PCode or entity CLOSING CONNECTION")
	serverSocket.close()
		
repeat = randint(5,20)
udp_port = randint(20000,30000)
len = randint(50,100)
codeA = randint(100,400)
ENTITY2 = 2
dLength = 12
print("sending to the client: data_len: {} pcode: {} entity: {} repeat: {} udp_port: {} len: {} codeA: {}".format(dLength, pCode, ENTITY2, repeat, udp_port, len, codeA))
phaseAS = struct.pack("!IHHIIHH", dLength, pCode, ENTITY2, repeat, udp_port, len, codeA)
serverSocket.sendto(phaseAS, clientAddress)
#start listening on udp_port sent to client

serverSocket.close()

serverSocket2 = socket(AF_INET, SOCK_DGRAM)
serverSocket2.bind(("",udp_port))
print("SERVER: Server ready on the new UDP port: {}".format(udp_port))
print("SERVER:------------------ End of Stage A ------------")
print()
print("SERVER:----------------- Starting Stage B -----------")

while True:
	#may have to add 3 sec timeout here 
	phaseBC, clientAddress = serverSocket2.recvfrom(1024)
	dLength2, pCode, ENTITY, packet_id, data = struct.unpack('!IHHIs', phaseBC)
	print("SERVER: received_packet_id = {} data_len = {} pcode: {}".format(packet_id,dLength2,pCode))
	
	if(dLength2 % 4 != 0):
		print("Incorect data length CLOSING CONNECTION")
		serverSocket2.close()
	
	if(pCode != codeA or ENTITY != 1):
		print("incorect PCode or entity CLOSING CONNECTION")
		serverSocket2.close()
	
	if(packet_id == repeat - 1):
		break
	
	coin = randint(0,1)
	dLength = 4

	if (coin == 1):
		print("Sending acknowledgement")
		acked_packet_id = packet_id + 1
		ackStruct = struct.pack('!IHHI',dLength,pCode,ENTITY2,acked_packet_id)
		serverSocket2.sendto(ackStruct,clientAddress)

	

sys.exit()#Terminate the program after sending the corresponding data
