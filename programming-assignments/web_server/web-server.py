from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000
serverName = "localhost"
serverSocket.bind((serverName, serverPort))
serverSocket.listen(10)

while True:
    print("ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    # print(addr)
    try:
        message = connectionSocket.recv(1024).decode()
        # print(message)
        filename = message.split()[1][1:]
        with open(filename) as file:
            outputdata = file.readlines()
        connectionSocket.sendall("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.sendall("\r\n".encode())   # the end of header
        for i in range(len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        print("file not found")
        connectionSocket.sendall("HTTP/1.1 404 not found\r\n".encode())
        connectionSocket.sendall("\r\n".encode())
        connectionSocket.close()

    
    
        

    