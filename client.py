import socket
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "127.0.0.1"
# the port number
port = 5001
# the name of file we want to send
filename = "SampleJPGImage_50kbmb.jpg"
# get file size
filesize = os.path.getsize(filename)

# create the client socket
client = socket.socket()

print(f"[+] Connecting to {host}:{port}")
client.connect((host, port))
print("[+] Connected.")

# send the filename and filesize
client.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file

with open(filename, "rb") as file:
    while True:
        # read the bytes from the file
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in busy networks
        client.sendall(bytes_read)


client.close()
