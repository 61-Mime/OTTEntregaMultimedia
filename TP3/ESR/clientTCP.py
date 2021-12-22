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
    # if reRouting and isFinalNode:
    #     sock.recv(buff_size).decode()
    #     sock.sendall('OK'.encode())

    if not isFinalNode:
        # recebe destinos
        # destinies = sock.recv(buff_size).decode()
        # print('Destinos:', destinies)
        # sock.sendall(destinies.encode())
        destinies = stats[1]
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
    # recebe origem
        # origin = sock.recv(buff_size).decode()
        # print('Origem:', origin)
        # sock.sendall(origin.encode())
        # # recebe metrica
        # metric = eval(sock.recv(buff_size).decode())
        # print('Metrica:', metric)
        # sock.sendall(str(metric).encode())


def clientTCPListening(message, server, sock, neighboursList, destinies, origin, metric):

    server_address = (server, 8080)
    print('[TCP]connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:

        print('[TCP]sending "%s"' % message)
        messageToBytes = str.encode(message)
        sock.sendall(messageToBytes)
        isFinalNode = False
        reRouting = False

        while True:
            data = sock.recv(buff_size).decode()
            print('[TCP]received "%s"' % data)
            stats = data.split('|')

            if stats[0] == 'Sending route info.':
                    # sock.sendall('OK'.encode())
                    # print('------------------', reRouting)

                    reRouting = routeTable(isFinalNode, destinies, sock, origin, metric, stats)

            else:
                # recebe vizinhos da topologia
                data = eval(data)
                neighboursList = data
                # recebe vizinhos que estão conectados
                neighboursConnected = isNeighbourConnected(sock)
                # recebe booleano identificativo de nodo final
                isFinalNode = eval(sock.recv(buff_size).decode())
                sock.sendall('Received final node value'.encode())
                print('[TCP] Final Node:', sock.recv(buff_size).decode())

                if isFinalNode:
                    sock.sendall('I want the stream'.encode())
                    print('[TCP]', sock.recv(buff_size).decode())
                    sock.sendall('Waiting for stream...'.encode())
                    print('Waiting for stream...')
                else:
                    sock.sendall('Update Routes'.encode())
            # clientUDP.udpClientListening(neighboursConnected, isFinalNode)

    finally:
        print('[TCP]Closing Socket...')
