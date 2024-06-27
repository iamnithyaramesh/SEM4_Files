from twisted.internet import reactor, protocol

# This class handles connections from clients
class ChatServer(protocol.Protocol):
    def __init__(self,factory):
        self.factory=factory
    def connectionMade(self):
        self.factory.clients.append(self)
        print("Client connected")

    def dataReceived(self, data):
        print(f"Received message: {data.decode()}")
        for client in self.factory.clients:
            if client != self:  
                client.transport.write(data)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected")

# This factory creates instances of the ChatServer
class ChatServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        
        return ChatServer(self)

if __name__ == '__main__':
    reactor.listenTCP(5000, ChatServerFactory())
    print("Chat server started on port 5000")
    reactor.run()
