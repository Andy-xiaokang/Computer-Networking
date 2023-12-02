from socket import *
serverName = "127.0.0.1"
severPort = 12000
clientsocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input lowercase sentence:")
clientsocket.sendto(message.encode(), (serverName, severPort))
modifiedMessage, serverAddress = clientsocket.recvfrom(2048)
print(modifiedMessage.decode())
clientsocket.close()


