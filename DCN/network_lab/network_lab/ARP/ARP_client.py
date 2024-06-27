from twisted.internet import reactor, protocol

class ARPClient(protocol.Protocol):
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def connectionMade(self):
        self.transport.write(self.ip_address.encode())

    def dataReceived(self, data):
        print(data.decode())
        self.transport.loseConnection()

class ARPClientFactory(protocol.ClientFactory):
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def buildProtocol(self, addr):
        return ARPClient(self.ip_address)

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection to server failed: {reason.getErrorMessage()}")
        reactor.stop()

def run_arp_client(ip_address):
    host = "localhost"
    port = 8000
    factory = ARPClientFactory(ip_address)
    reactor.connectTCP(host, port, factory)
    print(f"Connecting to ARP server at {host}:{port}...")
    reactor.run()

if __name__ == "__main__":
    ip_address_to_resolve = "192.168.1.2"  # IP address to resolve
    run_arp_client(ip_address_to_resolve)
