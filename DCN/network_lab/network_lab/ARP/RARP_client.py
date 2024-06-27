from twisted.internet import reactor, protocol

class RARPClient(protocol.Protocol):
    def __init__(self, mac_address):
        self.mac_address = mac_address

    def connectionMade(self):
        self.transport.write(self.mac_address.encode())

    def dataReceived(self, data):
        print(data.decode())
        self.transport.loseConnection()

class RARPClientFactory(protocol.ClientFactory):
    def __init__(self, mac_address):
        self.mac_address = mac_address

    def buildProtocol(self, addr):
        return RARPClient(self.mac_address)

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection to server failed: {reason.getErrorMessage()}")
        reactor.stop()

def run_rarp_client(mac_address):
    host = "localhost"
    port = 9000
    factory = RARPClientFactory(mac_address)
    reactor.connectTCP(host, port, factory)
    print(f"Connecting to RARP server at {host}:{port}...")
    reactor.run()

if __name__ == "__main__":
    mac_address_to_resolve = "0a:bc:de:f0:12:34"  # MAC address to resolve
    run_rarp_client(mac_address_to_resolve)
