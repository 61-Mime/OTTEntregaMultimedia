import socket

localIP = "127.0.0.1"

localPort = 7070

serverAddressPort = ("10.0.0.10", 7070)

bufferSize = 20480

def udpClientListening(server):

    while True:
        data = server.udpSocket.recvfrom(bufferSize)
        server.queue.append(data[0])

def udpClientSending(server):

    while True:

        while(len(server.queue) == 0):
            pass

        firstQueueElement = server.queue[0]
        server.queue = server.queue[1:]

        if server.destinies:
            for e in server.destinies:
                server.udpSocket.sendto(firstQueueElement, (e, 7070))
        else:
            server.udpSocket.sendto(firstQueueElement, (localIP, 6060))
