from twisted.internet import reactor,protocol

class ChatServer(protocol.Protocol):

    def __init__(self,factory):
        self.factory=factory

    def connectionMade(self):
        self.factory.clients.append(self)
        print("Connected")
    
    def dataReceived(self, data):
        print(f"Received message:{data.decode()}")
        for client in self.factory.clients:
            if client!=self:
                client.transport.write(data)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Lost")

class ChatServerFactory(protocol.Factory):
    def __init__(self):
        self.clients=[]
    
    def buildProtocol(self, addr):
        return ChatServer(self)
    
if __name__=='__main__':
    reactor.listenTCP(5000,ChatServerFactory())
    print('Chat started')
    reactor.run()

