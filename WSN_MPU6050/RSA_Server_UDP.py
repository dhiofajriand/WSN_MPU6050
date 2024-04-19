import accessor.upsertData as upsert
import accessor.getData as get
import socket
import time
import datetime
#1import smbus
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

SERVER = "192.168.43.150"
PORT = 5060
BUFFERSIZE = 1024

#Generate RSA Key Pair
key_pair = RSA.generate(2048)
private_key = key_pair.export_key()
public_key = key_pair.publickey().export_key()

#Create UDP Socket
server=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER, PORT))
print("UDP SERVER UP AND LISTENING")

#Server Waiting Client Address
data, client_address = server.recvfrom(BUFFERSIZE)
print("CLIENT IDENTIFIED")

#Server sending public key
server.sendto(public_key, client_address)
print("KEY SENT")

#Data Communication
while True:
	#Receive encrypted data from the client
	data, client_address = server.recvfrom(BUFFERSIZE)
	
	# Create cipher object with the server's private key
	cipher = PKCS1_OAEP.new(key_pair)

	# Decrypt the received data
	decrypted_data = cipher.decrypt(data)

	# Process the decrypted data as needed
	print("Received data:", decrypted_data.decode())

	msg_array = decrypted_data.split()
	
	print("Data Received ;)")
	print(decrypted_data)
	
	Ax = float(msg_array[0])
	Ay = float(msg_array[1])
	Az = float(msg_array[2])
	
	print(Ax, Ay, Az)
	
	now = int(round(time.time()*1000))
	date = str(datetime.datetime.fromtimestamp(now/1000.0).date())
	day = date.split("-")[2]
	if day != get.getLatestDate():
		upsert.insert(Ax, Ay, Az)
	else:
		idd = float(get.getLatestId())
		print(idd)
		upsert.updateData(idd, Ax, Ay, Az)