import accessor.upsertData as upsert
import accessor.getData as get
import time
import socket 
import threading
import datetime

HEADER = 64
PORT = 5050
SERVER = "192.168.43.149"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    i = 0
    connected = True
    total_byte = 0
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            print("Enter msg_length")
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break
            total_byte += len(msg)
            print("msg = ", msg)
            msg_array = msg.split()
            print("msg array = ", msg_array)
            Ax = float(msg_array[0])
            Ay = float(msg_array[1])
            Az = float(msg_array[2])

            now = int(round(time.time() * 1000))
            date = str(datetime.datetime.fromtimestamp(now/1000.0).date())
            day = date.split("-")[2]
            if day != get.getLatestDate():
                upsert.insert(Ax, Ay, Az)
            else:
                idd = get.getLatestId()
                upsert.updateData(idd, Ax, Ay, Az)
            conn.send("Msg received".encode(FORMAT))
    print (total_byte)
    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print("Key Sent")
        handle_client(conn,addr)

print("[STARTING] server is starting..")
start()