import json
import serverTCP
import socket
import clientUDP
from threading import Thread

class OttServer:

    def __init__(self, serverAddress, topology, connected, overlay):
        self.serverAddress = serverAddress
        self.topology = topology
        self.connected = connected
        self.overlay = overlay
        self.routes = []
        self.destinies = []
        self.clientThreads = {}
        self.queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udpSocket.bind(('', 7070))

    def connectUDPListening(self, server):
        clientUDP.udpClientListening(server)

    def connectUDPSending(self, server):
        clientUDP.udpClientSending(server)

    def beginUDP(self, server):
        threadListening = Thread(target=self.connectUDPListening, args=(server,))
        threadSending = Thread(target=self.connectUDPSending, args=(server,))

        threadListening.start()
        threadSending.start()

    def addClientThread(self, client_address, connection):
        self.clientThreads[client_address] = connection

    def serverDestinies(self):
        self.destinies = []

        for route in self.routes:
            for node in range(len(route)):
                if route[node] == self.serverAddress:
                    self.destinies.append(route[node + 1])

        self.destinies = set(self.destinies)
        self.destinies = list(self.destinies)

    def nodeDestinies(self, originNode):
        destinies = []

        for route in self.routes:
            for node in range(len(route)):
                if route[node] == originNode:
                    destinies.append(route[node + 1])

        destinies = set(destinies)
        destinies = list(destinies)

        return destinies

    def findMetric(self, node):

        for route in self.routes:
            try:
                metric = route.index(node)
            except:
                pass

        return metric

    def creatRouteInfo(self):
        routeInfo = {}
        finalNodes = self.getFinalNodes()

        self.serverDestinies()
        routeInfo[self.serverAddress] = self.destinies

        for node in self.topology:
            if node not in finalNodes and node != self.serverAddress and node in self.connected:
                routeInfo[node] = self.nodeDestinies(node)

        return routeInfo

    def sendRouteStats(self, destiny, finalNodes, routeInfo, connection, originNode):
        if destiny not in finalNodes:
            # envia destinos
            print(destiny, 'routeInfo[destiny]:', routeInfo[destiny])

            connection.sendall(('Sending route info.|' + str(routeInfo[destiny]) + '|' + str(originNode) + '|' + str(self.findMetric(destiny))).encode())

        else:
            connection.sendall(('Sending route info.|' + str(originNode) + '|' + str(self.findMetric(destiny))).encode())

    def sendingRouteInfo(self):
        finalNodes = self.getFinalNodes()
        routeInfo = self.creatRouteInfo()
        print('Route Info:', routeInfo)

        for originNode in routeInfo:
            if originNode not in finalNodes:
                for destiny in routeInfo[originNode]:
                    connection = self.clientThreads[destiny]
                    self.sendRouteStats(destiny, finalNodes, routeInfo, connection, originNode)

        print('[TCP] Route Info sent to all nodes.')

    def getFinalNodes(self):
        res = []

        for e in self.topology:
            if len(self.topology[e]) == 1 and e != self.serverAddress and e in self.connected:
                res.append(e)

        return res

    def updateRoutes(self):
        self.routes = []

        finalNodes = self.getFinalNodes()

        for finalNode in finalNodes:
            route = self.createRoute(finalNode)
            if route not in self.routes:
                self.routes.append(route)

        print('Updated routes:', self.routes)
        self.sendingRouteInfo()

    def createRoute(self, finalNode):
        explored = []

        # Queue for traversing the
        # graph in the BFS
        queue = [[self.serverAddress]]

        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Condition to check if the
            # current node is not visited
            if node not in explored:
                neighbours = self.overlay[node]

                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    # Condition to check if the
                    # neighbour node is the goal
                    if neighbour == finalNode:
                        self.routes.append(new_path)
                        return new_path
                explored.append(node)

        # Condition when the nodes
        # are not connected
        print("So sorry, but a connecting"\
                    "path doesn't exist :(")
        return []

    def searchConnected(self, nodeList, overlay, e, size):
        l = []
        i = []
        res = overlay
        while (size > 0) and overlay == []:
            for n in nodeList:
                i = [t for t in self.connected if t in self.topology[n]]
                if len(i) > 1:
                    if e in i:
                        i.remove(e)
                        for elem in i:
                            res.append(elem)
                    else:
                        for elem in i:
                            res.append(elem)
                else:
                    if e not in i and len(i) == 1:
                        for elem in i:
                            res.append(elem)

                    else:
                        for elem in self.topology[n]:
                            l.append(elem)
                        if e in l:
                            l.remove(e)
            size -= 1

            if not overlay:
                self.searchConnected(l, res, e, size)

        res = set(res)
        res = list(res)

        return res

    def createOverlay(self):
        self.overlay = {}
        size = len(self.topology)
        i = []
        res = []

        for e in self.connected:
            i = [n for n in self.connected if n in self.topology[e]]
            if i:
                self.overlay[e] = i
                nonConnectedNodes = [nc for nc in self.topology[e] if nc not in i]

                if len(nonConnectedNodes) > 0:
                    res = self.searchConnected(nonConnectedNodes, [], e, size)
                    for elem in res:
                        if elem not in self.overlay[e]:
                            self.overlay[e].append(elem)
            else:
                self.overlay[e] = []
                self.overlay[e] = self.searchConnected(self.topology[e], self.overlay[e], e, size)

        print('Overlay Network:', self.overlay)

    def addConnected(self, client_address):
        self.connected.append(client_address)

    def removeConnected(self, client_address):
        self.connected.remove(client_address)

with open('cenario2.json') as topologia:
    topology = json.load(topologia)
server = OttServer("10.0.0.10", topology, ['10.0.0.10'], {"10.0.0.10":""})

threadTCP = Thread(target=serverTCP.serverTCPListening, args=(topology, server))
threadUDP = Thread(target=server.beginUDP, args=(server,))

threadTCP.start()
threadUDP.start()
