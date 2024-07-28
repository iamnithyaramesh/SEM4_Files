
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class EchoUDP(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        print(f"Received datagram from {address}: {datagram.decode()}")

        # Echo back the received datagram to the sender
        self.transport.write(datagram, address)
        print(f"Echoed back to {address}: {datagram.decode()}")

def main():
    reactor.listenUDP(8000, EchoUDP())
    print("Listening on port 8000...")
    reactor.run()

if __name__ == '__main__':
    main()
