import socket
import sys
from threading import Thread
import time
import serverUDP

localIP     = "10.0.0.10"

localPort   = 8080

bufferSize  = 4096

def findNeighbours(topology, client_address):
    return topology[client_address]

def nodesToConnect(client_address, server, topology):
    neighbours = topology[client_address]
    toConnect = []
    for n in neighbours:
        if n in server.connected:
            toConnect.append(n)

    if not toConnect:
        toConnect.append(server.serverAddress)

    return toConnect

def connectionClient(connection, client_address, topology, server):
    try:
        print('[TCP]connection from', client_address[0])
        server.addConnected(client_address[0])
        server.createOverlay()

        while True:
            data = connection.recv(bufferSize).decode()
            print('[TCP]received "%s"' % data, 'from', client_address[0])

            if data == 'I want to connect to server':
                connection.sendall(str(findNeighbours(topology, client_address[0])).encode())

            elif data == 'Leaving...':
                print('[TCP]Client %s is leaving...' % client_address[0])
                server.removeConnected(client_address[0])
                server.createOverlay()
                server.updateRoutes()
                break

            elif data == 'Neighbours connected?':
                finalNode = False
                if len(topology[client_address[0]]) == 1:
                    finalNode = True
                nodes = nodesToConnect(client_address[0], server, topology)
                print('Sending neighboursConnected...')
                # envia vizinhos conectados
                connection.sendall(str(nodes).encode())
                print(client_address[0], connection.recv(bufferSize).decode())
                # envia booleano que identifica se o nodo é final ou não
                connection.sendall(str(finalNode).encode())
                print(client_address[0], connection.recv(bufferSize).decode())
                connection.sendall('OK'.encode())

            elif data == 'Update Routes':
                server.updateRoutes()

            elif data == 'I want the stream':
                connection.sendall('OK'.encode())
                print('[TCP] :', connection.recv(bufferSize).decode())
                server.updateRoutes()


    finally:
        # Clean up the connection
        connection.close()


def serverTCPListening(topology, server):

    sock = server.socket

    sock.bind(('', localPort))

    sock.listen(0)

    while True:
        print('[TCP]waiting for a connection')
        connection, client_address = sock.accept()

        threadTCP = Thread(target=connectionClient, args=(connection, client_address, topology, server))

        server.addClientThread(client_address[0], connection)

        threadTCP.start()

    sock.close()
