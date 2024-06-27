from twisted.internet import reactor, protocol

PORT = 5000

class MyServer(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b"Connection with the server established!")
        print("Client connected.")
    
    def dataReceived(self, data):
        self.transport.write(data)

class MyServerFactory(protocol.Factory):
    protocol = MyServer()

factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()

