import socket
import os
import threading
import time

# device's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# Keep track of all connected device
# s
connected_devices = []

# create the server socket
# TCP socket
server = socket.socket()

# bind the socket to our local address
server.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
server.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = server.accept()

thread = threading.Thread()
thread.start()
print(f"[ACTIVE CONNECTIONS] {threading.active_count()}")

# Add the new connection to all connected_devices
connected_devices.append(address)
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
beginTime = time.time()
# print the current timestamp
print("[BEGIN RECEIVING]", beginTime)

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)

filename = "SampleJPGImage_50kbmb.jpg"
print(filename)
filesize = os.path.getsize(filename)
print('file size in bytes:', filesize)

# start receiving the file from the socket

with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
    endTime = time.time()
    print("[END RECEIVING]", endTime)

print("Total Time in Microseconds:", (endTime - beginTime)*1000000)
filesize = os.path.getsize(filename)
print('file size in bytes:', filesize)
# close the client socket
client_socket.close()
# close the server socket
server.close()
