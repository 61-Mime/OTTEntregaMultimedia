
class ClientHandler:
    def __init__(self, clients):
        # super(clientHandler, self).__init__()
        self.clients = clients

    def addClient_resetTime(self, client_address):
        self.clients.append(client_address)

    def deleteClient(self, client_address):
        self.clients.remove(client_address)
