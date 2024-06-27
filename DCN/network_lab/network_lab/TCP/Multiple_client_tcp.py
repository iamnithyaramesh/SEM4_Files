# from twisted.internet import reactor, protocol

# HOST = 'localhost'
# PORT = 5000

# class MyClient(protocol.Protocol):
#     def connectionMade(self):
#         print ("connected!")

#     def dataReceived(self, data):
#         print(data.decode())
#         self.transport.write(input(':::: ').encode())
#         print(data.decode())

# class MyClientFactory(protocol.ClientFactory):
#     protocol = MyClient

# factory = MyClientFactory()
# reactor.connectTCP(HOST, PORT, factory)

# reactor.run()

from twisted.internet import reactor, protocol

HOST = 'localhost'
PORT = 5000

class MyServer(protocol.Protocol):
    def connectionMade(self):
        print("New client connected.")
        self.factory.clients.append(self)

    def dataReceived(self, data):
        print(f"Received message: {data.decode()}")
        for client in self.factory.clients:
            if client != self:
                client.transport.write(data)

    def connectionLost(self, reason):
        print("Client disconnected.")
        self.factory.clients.remove(self)

class MyServerFactory(protocol.Factory):
    protocol = MyServer
    def __init__(self):
        self.clients = []

factory = MyServerFactory()
reactor.listenTCP(PORT, factory)

print(f"Server listening on {HOST}:{PORT}")
reactor.run()
