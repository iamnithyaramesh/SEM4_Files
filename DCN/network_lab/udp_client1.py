from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class EchoClient(DatagramProtocol):
    def __init__(self, message):
        self.message = message

    def startProtocol(self):
        host = "127.0.0.1"
        port = 12345
        self.transport.connect(host, port)
        print(f"Sending {self.message}")
        self.transport.write(self.message.encode())

    def datagramReceived(self, data, addr):
        print(f"Received response: {data.decode()}")
        reactor.stop()

def main():
    # Hardcode the message for simplicity
    message = "Hello, UDP server client1!"
    reactor.listenUDP(0, EchoClient(message))
    reactor.run()

if __name__ == '__main__':
    main()
