import socket

localIP = "127.0.0.1"

localPort = 7070

serverAddressPort = ("10.0.0.10", 7070)

bufferSize = 20480

# socket, queue
def udpClientListening(server):
    # neighboursList = cleanNeighbours(neighboursList)
    # print('[UDP]', neighboursList)



    while True:
        data = server.udpSocket.recvfrom(bufferSize)
        server.queue.append(data[0])

    # msg = "[UDP]Message from Server {}".format(msgFromNode)

    # print(msg)

# self.destiny, self.queue, self.udpSocket
def udpClientSending(server):

    while True:

        # print('destiniesUDP', server.destinies)
        # print('queueUDP', server.queue)

        while(len(server.queue) == 0):
            pass

        firstQueueElement = server.queue[0]
        server.queue = server.queue[1:]

        # print('CLOCKCLOCKCLOCKCLOCKCLOCKCLOCK')
        print('destinies UDP:', server.destinies)
        # print(type(eval(server.destinies)))
        if server.destinies:
            for e in server.destinies:
                print(e)
                server.udpSocket.sendto(firstQueueElement, (e, 7070))
        else:
            server.udpSocket.sendto(firstQueueElement, (localIP, 6060))
