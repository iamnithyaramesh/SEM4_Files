from twisted.internet import reactor, protocol

class ChatServer(protocol.DatagramProtocol):
    def __init__(self):
        self.clients = {}

    def datagramReceived(self, data, addr):
        message = data.decode()
        if message.startswith("username:"):
            username = message.split(":")[1]
            self.clients[addr] = username
            print(f"{username} joined the chat.")
        else:
            sender_username = self.clients.get(addr, "Unknown")
            message_to_send = f"{sender_username}: {message}"
            for client_addr in self.clients:
                if client_addr != addr:
                    self.transport.write(message_to_send.encode(), client_addr)

def main():
    reactor.listenUDP(9999, ChatServer())
    print("UDP Chat Server started on port 9999...")
    reactor.run()

if __name__ == '__main__':
    main()
