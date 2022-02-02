# Import socket module
from socket import * 
import sys # In order to terminate the program

# import struct to create the following sctruct as specified
from struct import *
from random import *

# returns udp_port, packetA (struct)
def phaseA(packet, serverSocket):

	

	data_length, PCODE, ENTITY, data = unpack("!IHH24s", packet)

	checkMsg = "hello world!!!00"
	temp = data.decode()
	# temp = temp.replace("0", "")	
	print(temp + " this is temp")
	temp2 = temp.strip("0")
	print(temp2 + " this is t emp2")
	# checks for server to terminate socket connection
	if (data_length % 4 != 0 ):
		print("CLOSING SOCKET")
		serverSocket.close()
	if (PCODE != 0):
		print("CLOSING SOCKET2")
		serverSocket.close()
	if (str(temp) == checkMsg.lower()):
		print(temp)
		print("CLOSING SOCKET3")
		print(checkMsg.lower())
		serverSocket.close()
	if(ENTITY != 1):
		print("CLOSING SOCKET4")
		serverSocket.close()

	repeat = randint(5,20)
	udp_port = randint(20000, 30000)
	aLen = randint(50,100)
	codeA = randint(100, 400)
	ENTITY = 2
	"""
	STRUCT:::::

	data_length ==> len(data)
	pcode == 0
	entity ==> 2 
	repeat ==> random integer (4 bytes) between 5 and 20
	udp_port ==> random integer (4 bytes) between 20000 and 30000
	len  ==> short random number between 50 and 100
	codeA ==> short random number between 100 and 40
	"""

	print("sending to the client: data_length: {}  code: {}  entity: {} repeat: {} udp_port: {}  len: {} codeA: {}".format(
		data_length, codeA, ENTITY, repeat, udp_port, aLen, codeA))

	packet = pack("!IHHIIHH", data_length, PCODE, ENTITY, repeat, udp_port, aLen, codeA)

	return udp_port, packet, repeat

	# end of phase a check

#return sendingPacket, repeatDone and PacketB1 (sever reply)
def phaseBSend(packet, serverSocket, repeat):
	repeatDone = False
	sendingPacket = False

	data_length, PCODE, ENTITY, packetID, data = unpack("!IHHIs", packet)

	print("SERVER: received_packet_id =  {} data_len =  {} pcode: {}".format(packetID, data_length, PCODE))


	if (data_length % 4 != 0 ):
		print("CLOSING SOCKET")
		serverSocket.close()
	if (PCODE != 0):
		print("CLOSING SOCKET2")
		serverSocket.close()
	if(ENTITY != 1):
		print("CLOSING SOCKET4")
		serverSocket.close()

	ack = randint(0,1)


	if (ack == 1 ): 
		sendingPacket = True
	ak_packet_id = packetID

	if (ak_packet_id == repeat -1):
		repeatDone = True

	"""
	Struc

	data_len
	pcode = codeA
	enty
	ak_packet_id -> packet id

	"""

	data_length = 4
	ENTITY = 2

	print("SERVER: received_packet_id =  {} data_len =  {}  pcode: {}".format(ak_packet_id, data_length, PCODE))
	packetB1 = pack("!IHHI", data_length, PCODE, ENTITY, ak_packet_id)

	return sendingPacket, repeatDone, packetB1;
	


# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# while True:

print('The server is ready to receive')

while True:

	firstPass, clientAddress = serverSocket.recvfrom(1024)
	# we check if it pases phase A
	udp_port, firstPassPacket, repeat= phaseA(firstPass, serverSocket)
	serverSocket.sendto(firstPassPacket, clientAddress)

	# listen to new udp_port FIXMEE
	serverSocket2 = socket(AF_INET, SOCK_DGRAM)
	serverSocket2.bind(("", udp_port))

	secondPass, clientAddress = serverSocket2.recvfrom(1024)


	sendingPacket, repeatDone, packetB1 = phaseBSend(secondPass, serverSocket2, repeat)

	while not repeatDone:

		if (sendingPacket):
			serverSocket2.sendto(secondPass, clientAddress)
			secondPass, clientAddress = serverSocket2.recvfrom(1024)
			sendingPacket, repeatDone, packetB1 = phaseBSend(secondPass, serverSocket2, repeat)
		else:
			secondPass, clientAddress = serverSocket2.recvfrom(1024)
			sendingPacket, repeatDone, packetB1 = phaseBSend(secondPass, serverSocket2, repeat)







serverSocket.close()  
sys.exit() 	#Terminate the program after sending the corresponding data
