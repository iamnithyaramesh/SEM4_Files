from twisted.internet import reactor, protocol

class ChatClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Connected to chat server.\n".encode())
        self.nickname = input("Enter your nickname: ")
        print("Type your messages, press Enter to send.")
        reactor.callInThread(self.message_loop)

    def dataReceived(self, data):
        print(data.decode(), end='')

    def message_loop(self):
        while True:
            message = input()
            if message:
                self.transport.write(f"<{self.nickname}> {message}\n".encode())

# This factory creates instances of the ChatClient
class ChatClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return ChatClient()

    def clientConnectionLost(self, connector, reason):
        print("Lost connection to the server.")
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

if __name__ == '__main__':
    port = 5000  # Should match the port the server is listening on
    reactor.connectTCP("localhost", port, ChatClientFactory())
    reactor.run()
