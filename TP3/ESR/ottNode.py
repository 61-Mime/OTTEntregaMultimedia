import clientTCP
import clientUDP
import socket
from threading import Thread

class OttNode:
    def __init__(self, neighboursList, bootstrapper):
        self.neighboursList = neighboursList
        self.bootstrapper = bootstrapper
        self.destinies = []
        self.origin = ''
        self.metric = 0
        self.queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udpSocket.bind(('', 7070))

    def connectToServer(self, server):
        clientTCP.clientTCPListening('I want to connect to server', server, self)

    def connectUDPListening(self):
        clientUDP.udpClientListening(self)

    def connectUDPSending(self):
        clientUDP.udpClientSending(self)

    def exitMessage(self):
        print('Leaving...')
        leaving = str.encode('Leaving...')
        self.socket.sendall(leaving)
        self.socket.close()

    def beginUDP(self):
        threadListening = Thread(target=self.connectUDPListening)
        threadSending = Thread(target=self.connectUDPSending)

        threadListening.start()
        threadSending.start()

    def initClient(self, server):
        threadTCP = Thread(target=self.connectToServer, args=(server,))
        threadTCP.start()
        self.beginUDP()
