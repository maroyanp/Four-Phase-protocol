# Import socket module
from socket import * 
import sys # In order to terminate the program

# import struct to create the following sctruct as specified
from struct import *
from random import *
import time


#return sendingPacket, repeatDone and PacketB1 (sever reply	

def phaseBSend(packet, serverSocket, repeat):
	repeatDone = False
	sendingPacket = False

	data_length, PCODE, ENTITY, packetID, data = unpack("!IHHIs", packet)

	# print("SERVER: received_packet_id =  {} data_len =  {} pcode: {}".format(packetID, data_length, PCODE))


	if (data_length % 4 != 0 ):
		print("CLOSING SOCKET")
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

	print("SERVER: received_packet_id =  {} data_len =  {}  pcode: {}".format(packetID, data_length, PCODE))
	packetB1 = pack("!IHHI", data_length, PCODE, ENTITY, ak_packet_id)
	print("----------------------------------------------------------------------------------------------------\n")
	print("SEVER: after packingB1", packetB1)

	return sendingPacket, repeatDone, packetB1;
	


# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# while True:

print('The server is ready to receive')

while True:

	# Server Phase A REC
	# --------------------------------------------------------------------------------
	firstPass, clientAddress = serverSocket.recvfrom(1024)
	# we check if it pases phase A

	data_length, PCODE, ENTITY, data = unpack("!IHH24s", firstPass)

	checkMsg = "hello world!!!00"
	temp = data.decode()
	# temp = temp.replace("0", "")	
	# print(temp + " this is temp")
	temp2 = temp.strip("0")
	# print(temp2 + " this is t emp2")
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

	p_sever_s_packetA = pack("!IHHIIHH", data_length, PCODE, ENTITY, repeat, udp_port, aLen, codeA)

	serverSocket.sendto(p_sever_s_packetA, clientAddress)

	print("::::::END OF STAGE A:::::::\n")

	# -----------------------------------------------------------------------------------------------
	# PHASE B-1 Rec

	print(":::::::Start Stage B:::::::::")
	serverSocket2 = socket(AF_INET, SOCK_DGRAM)
	serverSocket2.bind(("", udp_port))

	p_sever_r_packetB1, clientAddress= serverSocket2.recvfrom(1024)
	
	data_length, PCODE, ENTITY, packetID, data = unpack("!IHHIs", p_sever_r_packetB1)
	sendingPacket = False


	while (packetID < repeat):
		ack = randint(0,1)
		if (ack == 1 ): 
			sendingPacket = True
		"""
		Struc

		data_len
		pcode = codeA
		enty
		ak_packet_id -> packet id

		"""
		data_length2 = 4
		ENTITY = 2

		if (sendingPacket):
			print("SERVER: received_packet_id =  {} data_len =  {}  pcode: {}".format(packetID, data_length, PCODE))

			p_sever_s_packetB1 = pack("!IHHI", data_length2, PCODE, ENTITY, packetID)
			# print("------------------------------------------------------------------------------\n")
			serverSocket2.sendto(p_sever_s_packetB1, clientAddress)
			packetID += 1

		# time.sleep(5)

	# after reciving all the rpeat packs B2

	"""
	Struck B2

	data_len
	pcode = codeA
	entity
	tcp_port ==>> random integer (4 bytes) between 20000 and 30000
	codeB ==>> random integer number between 100 and 400

	"""
	tcp_port = randint(20000, 30000)
	codeB = randint(100, 400)
	p_sever_s_packetB2 = pack("!IHHII", data_length, PCODE, ENTITY, tcp_port, codeB)

	print(" ------------- B2: sending tcp_port {}  codeB {}".format(tcp_port, codeB))
	serverSocket2.sendto(p_sever_s_packetB2, clientAddress)
	serverSocket2.close()
	print(" ------------ End of Stage B  ------------\n")
	# serverSocket.close()	

	# END of phase B2
	# --------------------------------------------------------------------------------------------------
	#phase C
	print(" ------------ Stating Stage C ------------")
	s_tcpSocket = socket(AF_INET, SOCK_STREAM)

	# Bind the socket to server address and server port
	s_tcpSocket.bind(("", tcp_port))

	# Listen to at most 1 connection at a time
	s_tcpSocket.listen(5)

	# accepts client

	c_connect_c1, addr = s_tcpSocket.accept()
	time.sleep(5)
	print(" The server is ready to receive on tcp port:  {}".format(tcp_port))
	

	"""
	struct:
	data_len
	pcode = codeB
	entity = 2
	repeat2 --> random integer (4 bytes) between 5 and 20
	len2 --> int random number between 50 and 100
	codeC --> random Integer number between 100 and 400
	Char: any of the 26 characters in English alphabet: A to Z
	"""

	data_lengthC1 = 13
	PCODE = codeB
	ENTITY = 2
	repeat2 = randint(5,20)
	len2 = randint(50,100)
	codeC = randint(100,400)
	Rchar = chr(randint(ord('A'), ord('Z')))
	print(Rchar)


	p_sever_s_packetC1 = pack("!IHHIIIc", data_lengthC1, PCODE, ENTITY, repeat2, len2, codeC, Rchar.encode())
	print("Server Sending to the client:  data_length: {} code: {}  entity: {}  repeat2: {}  len2: {} codeC:  {}".format(
		data_lengthC1, PCODE, ENTITY, repeat2, len2, codeC))
	c_connect_c1.send(p_sever_s_packetC1)
	print("------------ End of Stage C    ------------\n")



