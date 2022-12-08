# import socket
#
#
# def client_program():
#     host = socket.gethostname()  # as both code is running on same pc
#     port = 5000  # socket server port number
#
#     client_socket = socket.socket()  # instantiate
#     client_socket.connect((host, port))  # connect to the server
#
#     message = input(" -> ")  # take input
#
#     while message.lower().strip() != 'bye':
#         client_socket.send(message.encode())  # send message
#         data = client_socket.recv(1024).decode()  # receive response
#
#         print('Received from server: ' + data)  # show in terminal
#
#         message = input(" -> ")  # again take input
#
#     client_socket.close()  # close the connection
#
#
# if __name__ == '__main__':
#     client_program()



# import socket
# ClientMultiSocket = socket.socket()
# host = '127.0.0.1'
# port = 2004
# print('Waiting for connection response')
# try:
#     ClientMultiSocket.connect((host, port))
# except socket.error as e:
#     print(str(e))
# res = ClientMultiSocket.recv(1024)
# while True:
#     Input = input('Hey there: ')
#     ClientMultiSocket.send(str.encode(Input))
#     res = ClientMultiSocket.recv(1024)
#     print(res.decode('utf-8'))
# ClientMultiSocket.close()

"""
import socket

host = '127.0.0.1'
port = 1233


ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Your message: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()

"""

import socket
import select
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # when there are no incoming data error is going to be raised
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()
