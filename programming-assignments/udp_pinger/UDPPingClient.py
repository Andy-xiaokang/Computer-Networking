import socket
import time

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_name = "localhost"
server_port = 12000

# Set the timeout value (in seconds) for the socket
timeout = 1  # Set the timeout to 1 second
client_socket.settimeout(timeout)

# Now you can use the UDP socket for sending/receiving data
# For example, to receive data:
for i in range(10):
    message = f"ping {i} {time.time()}"
    start_time = time.time()
    client_socket.sendto(message.encode(), (server_name, server_port))
    try:
        response, addr = client_socket.recvfrom(1024)
        end_time = time.time()
        print(response.decode() + f"  RTT {i}: {round((end_time - start_time)*1000, 3)} ms")
    except socket.timeout:
        print("Request time out")
        
client_socket.close()
