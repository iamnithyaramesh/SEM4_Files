from twisted.internet import reactor, protocol

class BusProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        print("New device connected: {}".format(self.transport.getPeer()))

        # Add device to list of connected devices
        self.factory.devices.append(self)

    def dataReceived(self, data):
        print("Received data from {}: {}".format(self.transport.getPeer(), data.decode()))

        # Broadcast data to all connected devices
        for device in self.factory.devices:
            if device is not self:
                device.transport.write(data)

    def connectionLost(self, reason):
        print("Device disconnected: {}".format(self.transport.getPeer()))

        # Remove device from list of connected devices
        self.factory.devices.remove(self)

class BusFactory(protocol.Factory):
    def __init__(self):
        self.devices = []

    def buildProtocol(self, addr):
        return BusProtocol(self)

if __name__ == '__main__':
    factory = BusFactory()
    reactor.listenTCP(8000, factory)
    reactor.run()
