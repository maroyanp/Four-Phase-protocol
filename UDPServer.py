# Import socket module
from socket import *
import struct 
import sys # In order to terminate the program
from struct import *
from random import *
import time

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
dLength, pCode, ENTITY, data = struct.unpack('!IHH16s', sentenceStruct)

decodeSentence = data.decode()
decodeSentence = decodeSentence.translate({ord('0'):None})
print("receiving from the client: data_len: {} pcode: {} entity: {} data: {}".format(dLength, pCode, ENTITY, decodeSentence))

if (dLength % 4 != 0):
	print("Incorect data length CLOSING CONNECTION")
	serverSocket.close()
		
if(decodeSentence != "Hello World!!!"):
	print("Incorect data CLOSING CONNECTION")
	serverSocket.close()
		
if(pCode != 0 or ENTITY != 1):
	print("incorect PCode or entity CLOSING CONNECTION")
	serverSocket.close()
		
repeat = randint(5,20)
udp_port = randint(20000,30000)
bLen = randint(50,100)
codeA = randint(100,400)
ENTITY2 = 2
dLength = 12

print("sending to the client: data_len: {} pcode: {} entity: {} repeat: {} udp_port: {} len: {} codeA: {}".format(dLength, pCode, ENTITY2, repeat, udp_port, bLen, codeA))
phaseAS = struct.pack("!IHHIIHH", dLength, pCode, ENTITY2, repeat, udp_port, bLen, codeA)
serverSocket.sendto(phaseAS, clientAddress)

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
	#print("SERVER: received_packet_id = {} data_len = {} pcode: {}".format(packet_id,dLength2,pCode))
	
	if(dLength2 % 4 != 0):
		print("Incorect data length CLOSING CONNECTION")
		serverSocket2.close()
	
	if(pCode != codeA or ENTITY != 1):
		print("incorect PCode or entity CLOSING CONNECTION")
		serverSocket2.close()
	
	coin = randint(0,1)
	dLength = 4

	if (coin == 1 or packet_id == repeat - 1):
		print("SERVER: received_packet_id = {} data_len = {} pcode: {}".format(packet_id,dLength2,pCode))
		acked_packet_id = packet_id
		ackStruct = struct.pack('!IHHI',dLength,pCode,ENTITY2,acked_packet_id)
		serverSocket2.sendto(ackStruct,clientAddress)
	
	if(packet_id == repeat - 1):
		break

dLength = 8
tcp_port = randint(20000,30000)
codeB = randint(100,400)

phaseB2Struct = struct.pack('!IHHII',dLength,pCode,ENTITY2,tcp_port,codeB)
serverSocket2.sendto(phaseB2Struct,clientAddress)
print("---------- B2: sending tcp_port {} codeB {}".format(tcp_port,codeB))

print("----------- End of Stage B -------------")
print()
print ("----------- Starting Stage C -----------")

serverSocket3 = socket(AF_INET, SOCK_STREAM)
serverSocket3.bind(("",tcp_port))
serverSocket3.listen(5)
connectionSocket, addr = serverSocket3.accept()
print("The server is ready to receive on tcp_port: {}".format(tcp_port))

dLength = 13
pCode = codeB
repeat2 = randint(5,20)
len2 = randint(5,20)
codeC = randint(100,400)
char = 'J' #make this random maybe

phaseCStruct = struct.pack('!IHHIIIc',dLength,pCode,ENTITY2,repeat2,len2,codeC,char.encode())
connectionSocket.send(phaseCStruct)
print("Server Sending to the client: data_len: {} pcode: {} entity: {} repeat2: {} len2: {} codeC: {} char: {}".format(dLength,pCode,ENTITY2,repeat2,len2,codeC,char))

print("----------- End of Stage C -------------")
print()
print ("----------- Starting Stage D -----------")

i = 0
print("Starting to Receive packets from client")

while i < repeat2:

	phaseDStruct = connectionSocket.recv(1024)
	temp = len(phaseDStruct)
	temp -= 8
	dLength2, pCode, ENTITY, data = struct.unpack('!IHH' + str(temp) + 's', phaseDStruct)

	data = data.decode()
	print("i = {} data_len: {} pcode: {} entity: {} data: {}".format(i, dLength2, pCode, ENTITY, data))
	i += 1

codeD = randint(100,400)
dLength = 4
pCode = codeC

finalPacket = struct.pack('!IHHI', dLength, pCode, ENTITY2, codeD)	
connectionSocket.send(finalPacket)

connectionSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
