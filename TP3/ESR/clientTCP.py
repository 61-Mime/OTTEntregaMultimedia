import socket
import sys
import atexit
import clientUDP

buff_size = 4096

def isNeighbourConnected(sock):
    sock.sendall(str('Neighbours connected?').encode())
    data = sock.recv(buff_size).decode()
    sock.sendall('Received neighbours that are connected.'.encode())
    return eval(data)

def routeTable(isFinalNode, destinies, sock, origin, metric, stats):

    if not isFinalNode:
        destinies = eval(stats[1])
        origin = stats[2]
        metric = stats[3]
        print('Destinos:', destinies)
        print('Origem:', origin)
        print('Metrica:', metric)
    else:
        origin = stats[1]
        metric = stats[2]
        print('Origem:', origin)
        print('Metrica:', metric)
    return destinies

def clientTCPListening(message, server, node):

    server_address = (server, 8080)
    print('[TCP]connecting to %s port %s' % server_address)
    node.socket.connect(server_address)

    try:

        print('[TCP]sending "%s"' % message)
        messageToBytes = str.encode(message)
        node.socket.sendall(messageToBytes)
        isFinalNode = False
        reRouting = False

        while True:
            data = node.socket.recv(buff_size).decode()
            print('[TCP]received "%s"' % data)
            stats = data.split('|')

            if stats[0] == 'Sending route info.':
                    node.destinies = routeTable(isFinalNode, node.destinies, node.socket, node.origin, node.metric, stats)
            else:
                # recebe vizinhos da topologia
                data = eval(data)
                node.neighboursList = data
                # recebe vizinhos que estão conectados
                neighboursConnected = isNeighbourConnected(node.socket)
                # recebe booleano identificativo de nodo final
                isFinalNode = eval(node.socket.recv(buff_size).decode())
                node.socket.sendall('Received final node value'.encode())
                print('[TCP] Final Node:', node.socket.recv(buff_size).decode())

                if isFinalNode:
                    node.socket.sendall('I want the stream'.encode())
                    print('[TCP]', node.socket.recv(buff_size).decode())
                    node.socket.sendall('Waiting for stream...'.encode())
                    print('Waiting for stream...')
                else:
                    node.socket.sendall('Update Routes'.encode())

    finally:
        print('[TCP]Closing Socket...')
