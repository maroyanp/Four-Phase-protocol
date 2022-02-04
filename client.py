# Import socket module
from socket import * 
import sys # In order to terminate the program
from struct import *
import struct
import time

def check_server_response(response):
    data_len, pcode, entity = struct.unpack_from('!IHH', response)
    if pcode==555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return 

# serverName = 'localhost'
# serverName = '99.250.87.197'
serverName = "34.69.60.253"
# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)
sentence = "Hello World!!!"
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
#change socket to be padded to for but for right now this should work ??
while (len(sentence) % 4 !=  0):
    sentence += '0'

sentence = bytearray(sentence, encoding="utf-8")
# after padding we can now send the data
packetSendA1 = pack('!IHH16s', len(sentence), PCODE, ENTITY, sentence)
clientSocket.sendto( packetSendA1, (serverName, serverPort))
# -------------------------------------------------------------------------------------------
# Phase A rec
#clientSocket.connect((serverName, serverPort))
packetA_Rec, serverAddress = clientSocket.recvfrom(2048)
clientSocket.close()
# -------------------------------------------------------------------------------------------
# Phase B-1 send
# creating new socket
clientSocket2 = socket(AF_INET, SOCK_DGRAM) 
check_server_response(packetA_Rec)
data_length, PCODE, ENTITY, repeat, udp_port, aLen, codeA = unpack('!IHHIIHH', packetA_Rec)

print("------------ Starting Stage A  ------------")
print(f"Received packet from server: data_len: {data_length}  pcode: {PCODE}  entity: {ENTITY}  repeat: {repeat}  len: {aLen}  udp_port: {udp_port}  codeA: {codeA}")
print("------------ End of Stage A  ------------\n")
print("------------ Starting Stage B  ------------")

ENTITY = 1
data  = bytearray(aLen)
PCODE = codeA
packetId = 0

data_length = aLen + 4

while (data_length % 4 != 0):
    data.append(0)
    data_length += 1

# print(data_length)
# now we continue to send till acknowlegment
# also we send and wait for a recive
while (packetId < repeat ):
    packetBsending = pack("!IHHI" + str(data_length) + "s" , data_length, PCODE, ENTITY, packetId,data)
    clientSocket2.sendto(packetBsending, (serverName, udp_port))
    
    try:
        clientSocket2.settimeout(5)
        p_clinet_r_B1, serverAddress = clientSocket2.recvfrom(2048)
        # print("reused data_kent")
        check_server_response(p_clinet_r_B1)
        data_length_B_r, PCODE_B_r, entit_b_r, ak_packet_id = unpack('!IHHI',p_clinet_r_B1)
        print("Received acknowledgement packet from server: data_len: {} pcode: {} entity: {} acknumber: {}".format(
            data_length_B_r, PCODE_B_r, entit_b_r, ak_packet_id))
        packetId += 1
    
    except:
        # time.sleep(5)
        continue #after 5 seconds?

# now recive from B2
p_clinet_r_B2, serverAddress = clientSocket2.recvfrom(2048)
clientSocket2.close()

data_length3, PCODE, ENTITY3, tcp_port, codeB =  unpack("!IHHII", p_clinet_r_B2)
print("Received final packet: data_len:  {} pcode:  {} entity: {}  tcp_port: {}  codeB: {}".format(
    data_length3, PCODE, ENTITY, tcp_port, codeB))
print("------------ End of Stage B  ------------\n")
# ------------------------------------------------------------------------------------------------------------
print("------------ Starting Stage C  ------------")

c_tcpSocket = socket(AF_INET, SOCK_STREAM)
print("connecting to server at tcp port {}".format(tcp_port))
c_tcpSocket.connect((serverName, tcp_port))
time.sleep(3)
p_client_r_C1 = c_tcpSocket.recv(1024)

data_lengthC1, PCODE, ENTITY, repeat2, len2, codeC, Rchar = unpack("!IHHIIIc",p_client_r_C1)
Rchar = Rchar.decode()

print(f"Received packet from server: data_len: {data_lengthC1}  pcode: {PCODE} " 
    +f"entity: {ENTITY} repeat2: {repeat2}   len2: {len2}   codeC: {codeC}   char:  {Rchar}")
print("------------ End of Stage C  ------------\n")
print("------------ Starting Stage D  ------------")

data_lengthD3 = len2
while(data_lengthD3 % 4 > 0 ):
    data_lengthD3 += 1

msg = ""
for i in range(data_lengthD3):
    msg += Rchar
PCODE = codeC
ENTITY = 1
print(f"sending  {msg} to server for {repeat2} times")
msg = bytearray(msg, encoding="utf-8")

"""
Struc
data_len -> len2 % 4
pcode = codeC
entity
data(filled with Rchar)
"""

p_client_s_D1 = pack("!IHH" + str(data_lengthD3) +"s", data_lengthD3, PCODE, ENTITY, msg)
for i in range(repeat2):
    c_tcpSocket.send(p_client_s_D1)
    time.sleep(1)

p_client_r_D2 = c_tcpSocket.recv(2048)
data_lengthD2, PCODE, entityD2, codeD = unpack("!IHHI", p_client_r_D2)
check_server_response(p_client_r_D2)
print(f"Received from server: data_len: {data_lengthD2}  pcode: {PCODE}  entity: {entityD2}  codeD: {codeD}")

c_tcpSocket.close()