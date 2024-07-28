from twisted.internet import reactor, protocol

class ChatClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect("127.0.0.1", 9999)  # Server IP and port
        self.username = input("Enter your username: ")
        self.transport.write(f"username:{self.username}".encode())

    def datagramReceived(self, data, addr):
        message = data.decode()
        print(message)

    def sendMessage(self):
        message = input("> ")
        if message.lower() == "/quit":
            self.transport.write(f"{self.username} has left the chat.".encode())
            reactor.stop()
        else:
            full_message = f"{self.username}: {message}"
            self.transport.write(full_message.encode())

def main():
    client = ChatClient()
    reactor.listenUDP(0, client)  # Choose a random available port for client
    reactor.callInThread(client.sendMessage)
    reactor.run()

if __name__ == '__main__':
    main()
