from twisted.internet import reactor, protocol

class StarClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")
        self.transport.write("Hello, server!".encode())

    def dataReceived(self, data):
        print("Received from server:", data.decode())
        self.transport.loseConnection()

class StarClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return StarClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

def main():
    # Connect to the server running on localhost (127.0.0.1) on port 8000
    factory = StarClientFactory()
    reactor.connectTCP("127.0.0.1", 8000, factory)
    reactor.run()

if __name__ == '__main__':
    main()
