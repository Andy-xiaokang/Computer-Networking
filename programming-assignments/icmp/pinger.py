from socket import *
import os
import sys  
import struct
import time  
import select 
import binascii  


ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum  
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        # fetch the ICMP header from the IP Packet
        icmp_header = recPacket[20:28]
        icmp_header_data = struct.unpack("bbHHh", icmp_header)
        print(len(icmp_header_data))
        print(icmp_header_data)
        
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request time out"
        
def sendOnePing(mySocket:socket, destAddr, ID):
    myChecksum = 0
    # print(ICMP_ECHO_REQUEST, myChecksum, ID)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(str(header + data))
    if sys.platform == "darwin":
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))
    
def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() - 20000
    # print(os.getpid())
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout = 1):
    dest = gethostbyname(host)
    print("Pinging " + dest + " using python")
    print("")
    while 1:
        delay = doOnePing(dest, timeout)
        print(delay)
        time.sleep(1)
    return delay

ping("google.com")