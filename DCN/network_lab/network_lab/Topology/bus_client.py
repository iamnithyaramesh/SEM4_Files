from twisted.internet import reactor, protocol

class BusClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")

    def dataReceived(self, data):
        print("Received data from server:", data.decode())

    def sendMessage(self, message):
        self.transport.write(message.encode())

class BusClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return BusClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

if __name__ == '__main__':
    # Connect to the server
    factory = BusClientFactory()
    reactor.connectTCP('127.0.0.1', 8000, factory)

    # Start the Twisted reactor loop
    reactor.run()
