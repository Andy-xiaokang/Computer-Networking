from socket import *
serverName = "127.0.0.1"
serverPort = 12000
clientServer = socket(AF_INET, SOCK_STREAM)
clientServer.connect((serverName, serverPort))
sentence = input("Input lowercase sentense:")
clientServer.send(sentence.encode())
modifiedSentence = clientServer.recv(1024)
print("From server: ", modifiedSentence.decode())
clientServer.close()