import socket



localIP     = "10.0.0.10"

localPort   = 8080

bufferSize  = 4096

# Create a datagram socket

def serverUDPListening():

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)



    # Bind to address and ip

    UDPServerSocket.bind(('', localPort))



    print("[UDP] server up and listening")



    # Listen for incoming datagrams

    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        message = bytesAddressPair[0]

        address = bytesAddressPair[1]

        clientMsg = "[UDP]Message from Client:{}".format(message)
        clientIP  = "[UDP]Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        UDPServerSocket.sendto('You are connected.'.encode(), address)
