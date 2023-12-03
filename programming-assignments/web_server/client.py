from socket import *
serverName = "localhost"
serverPort = 12000
clientServer = socket(AF_INET, SOCK_STREAM)
clientServer.connect((serverName, serverPort))
sentence = "GET /HelloWorld.html HTTP/1.1\r\n"
clientServer.send(sentence.encode())
while True:
    response = clientServer.recv(1024).decode()
    if len(response) == 0:
        break
    print(response)
clientServer.close()