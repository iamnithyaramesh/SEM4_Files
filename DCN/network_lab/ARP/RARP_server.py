# Purpose: RARP is used to map MAC addresses to IP addresses
from twisted.internet import reactor, protocol

class RARPServer(protocol.Protocol):
    def __init__(self, rarp_table):
        self.rarp_table = rarp_table

    def connectionMade(self):
        print("RARP Server connected")

    def dataReceived(self, data):
        mac_address = data.decode().strip()
        if mac_address in self.rarp_table:
            ip_address = self.rarp_table[mac_address]
            self.transport.write(f"IP address for {mac_address} is {ip_address}".encode())
        else:
            self.transport.write(f"No entry found for {mac_address}".encode())
        self.transport.loseConnection()

class RARPFactory(protocol.Factory):
    def __init__(self, rarp_table):
        self.rarp_table = rarp_table

    def buildProtocol(self, addr):
        return RARPServer(self.rarp_table)

def simulate_rarp():
    rarp_table = {
        "00:1a:2b:3c:4d:5e": "192.168.1.1",
        "0a:bc:de:f0:12:34": "192.168.1.2",
        "22:33:44:55:66:77": "192.168.1.3"
    }
    port = 9000
    reactor.listenTCP(port, RARPFactory(rarp_table))
    print(f"RARP server listening on port {port}")
    reactor.run()

if __name__ == "__main__":
    simulate_rarp()
