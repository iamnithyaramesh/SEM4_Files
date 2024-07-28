from twisted.internet import reactor, protocol

class RingClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")
        self.sendData()

    def dataReceived(self, data):
        print("Received data from server:", data.decode())
        self.transport.loseConnection()

    def sendData(self):
        message = input("Enter message to send: ").encode()
        self.transport.write(message)

class RingClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RingClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

if __name__ == '__main__':
    factory = RingClientFactory()
    reactor.connectTCP('localhost', 8000, factory)
    reactor.run()
