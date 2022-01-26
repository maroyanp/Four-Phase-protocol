# Import socket module
from socket import * 
import sys # In order to terminate the program

# import struct to create the following sctruct as specified
from struct import *
from random import *




"""
struct: 
    
    data_length --> 4 bytes (length of packet)
    pcode -> first phase == 0
    entity -> 2 bytes, (client uses 1 and server uses 2)
    data -> any siz % 4 == 0 (data must be padded until divisible by 4)

"""

# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

while True:

	print('The server is ready to receive')

	try:
		serverSocket.settimeout(3)

		sentenceStruct , clientAddress = serverSocket.recvfrom(1024)
		data_len, PCODE, ENTITY, data = unpack("!IIH20s", sentenceStruct)

		# check if divisable by 4:
		if (data_len % 4 != 0):
			print("message is not within protocol CLOSING CONNECTION")
			serverSocket.close
		

		capitalizedSentence = data.decode().upper()

		# phase A::
		"""
		repeat is a random integer (4 bytes) between 5 and 20
		udp_port is a random integer (4 bytes) between 20000 and 30000
		len is a short random number between 50 and 100
		codeA is a short random number  between 100 and 400
		The server then starts listening on the udp_port just sent to the client.

		"""
		repeat = randint(5,20)
		udp_port = randint(20000, 30000)
		aLen = randint(50,100)
		codeA = randint(100, 400)

		phaseA = pack("!IIHH", repeat, udp_port, aLen, codeA )
		serverSocket.sendto(phaseA, clientAddress)

		# serverSocket.sendto(capitalizedSentence.encode(), clientAddress)
		
	except:
		print("timed out connection nothing recived")
		serverSocket.close()
		break
		
	

	
	
	

serverSocket.close()  
sys.exit() 	#Terminate the program after sending the corresponding data
