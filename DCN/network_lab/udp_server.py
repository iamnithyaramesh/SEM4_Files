from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class EchoServer(DatagramProtocol):
    def datagramReceived(self, data, addr):
        print(f"Received {data.decode()} from {addr}")
        response = f"Echo: {data.decode()}"
        self.transport.write(response.encode(), addr)

def main():
    port = 12345
    reactor.listenUDP(port, EchoServer())
    print(f"UDP server listening on port {port}")
    reactor.run()

if __name__ == '__main__':
    main()
