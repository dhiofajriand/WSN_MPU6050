import smbus
import socket
import time

def send(msg):
    message = msg.encode()
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message)
    print(client_socket.recv(2048).decode(FORMAT))
    
def TCP (Ax,Ay,Az):
    final_data = "%f %f %f"%(Ax, Ay, Az)
    send (final_data)
   
def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
        
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

# Create client socket
PORT = 5050
HEADER = 64
SERVER = "192.168.43.150"
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ADDR))

total_data = 0
i = 0

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")
print ("Proses Kalibrasi")
i = 0
Ax1 = 0
Ay1 = 0
Az1 = 0
while (i<3000):
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    Ax1 += acc_x
    Ay1 += acc_y
    Az1 += acc_z
    i +=1
Ax1 /= 3000
Ay1 /= 3000
Az1 /= 3000
i = 0
total_data = 0

while True:
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    
    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = -1*((acc_x + (-1*Ax1))/16384.0)*9.80665
    Ay = -1*((acc_y + (-1*Ay1))/16384.0)*9.80665
    Az = -1*((acc_z + (-1*Az1))/16384.0)*9.80665
    
    if (Ax > -0.3 and Ax < 0.3):
        Ax = 0
    if (Ay > -0.3 and Ay < 0.3):
        Ay = 0
    if (Az > -0.3 and Az < 0.3):
        Az = 0
    
    print ("\tAx=%.2f m/s^2" %Ax, "\tAy=%.2f m/s^2" %Ay, "\tAz=%.2f m/s^2" %Az)
    final_data = "%f %f %f"%(Ax, Ay, Az)
    total_data += len(final_data)
    i += 1
    print ("Banyak data = " + str(i))
    print ("Total Data = " + str(total_data) + "Bytes")
    TCP(Ax,Ay,Az)
send(DISCONNECT_MESSAGE)