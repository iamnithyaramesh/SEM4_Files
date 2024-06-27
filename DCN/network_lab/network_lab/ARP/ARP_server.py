#Purpose: ARP is used to map IP addresses to MAC addresses

from twisted.internet import reactor, protocol

class ARPServer(protocol.Protocol):
    def __init__(self, arp_table):
        self.arp_table = arp_table

    def connectionMade(self):
        print("ARP Server connected")

    def dataReceived(self, data):
        ip_address = data.decode().strip()
        if ip_address in self.arp_table:
            mac_address = self.arp_table[ip_address]
            self.transport.write(f"MAC address for {ip_address} is {mac_address}".encode())
        else:
            self.transport.write(f"No entry found for {ip_address}".encode())
        self.transport.loseConnection()

class ARPFactory(protocol.Factory):
    def __init__(self, arp_table):
        self.arp_table = arp_table

    def buildProtocol(self, addr):
        return ARPServer(self.arp_table)

def simulate_arp():
    arp_table = {
        "192.168.1.1": "00:1a:2b:3c:4d:5e",
        "192.168.1.2": "0a:bc:de:f0:12:34",
        "192.168.1.3": "22:33:44:55:66:77"
    }
    port = 8000
    reactor.listenTCP(port, ARPFactory(arp_table))
    print(f"ARP server listening on port {port}")
    reactor.run()

if __name__ == "__main__":
    simulate_arp()
