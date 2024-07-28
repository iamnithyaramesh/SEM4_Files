from twisted.internet import reactor, protocol

class MeshProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.connections = []

    def connectionMade(self):
        print("New device connected: {}".format(self.transport.getPeer()))

        # Add device to list of connected devices
        self.factory.devices.append(self)
        self.connections.append(self)

        # Send connection information to all other devices
        for device in self.factory.devices:
            if device is not self:
                device.transport.write(str(self.transport.getPeer()).encode() + b" connected\n")

    def dataReceived(self, data):
        print("Received data from {}: {}".format(self.transport.getPeer(), data.decode()))

        # Send data to connected devices
        for device in self.connections:
            device.transport.write(data)

    def connectionLost(self, reason):
        print("Device disconnected: {}".format(self.transport.getPeer()))

        # Remove device from list of connected devices
        self.factory.devices.remove(self)
        self.connections.remove(self)

        # Send disconnection information to all other devices
        for device in self.factory.devices:
            if device is not self:
                device.transport.write(str(self.transport.getPeer()).encode() + b" disconnected\n")

class MeshFactory(protocol.Factory):
    def __init__(self):
        self.devices = []

    def buildProtocol(self, addr):
        return MeshProtocol(self)

if __name__ == '__main__':
    factory = MeshFactory()
    reactor.listenTCP(8000, factory)
    reactor.run()
