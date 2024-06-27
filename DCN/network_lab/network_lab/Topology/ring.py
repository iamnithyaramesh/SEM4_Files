from twisted.internet import reactor, protocol

class RingProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.successor = None

    def connectionMade(self):
        print("New device connected: {}".format(self.transport.getPeer()))

        if self.factory.devices:
            # Connect device to last device in list to form ring
            self.successor = self.factory.devices[-1]
            self.factory.devices[-1].successor = self

        self.factory.devices.append(self)

    def dataReceived(self, data):
        print("Received data from {}: {}".format(self.transport.getPeer(), data.decode()))

        for device in self.factory.devices:
            if device is not self:
                device.transport.write(data)

    def connectionLost(self, reason):
        print("Device disconnected: {}".format(self.transport.getPeer()))

        if self.successor:
            # Disconnect device from ring and connect successor to predecessor
            self.successor.factory.devices.remove(self)
            self.successor.successor = self.successor.factory.devices[self.successor.factory.devices.index(self)+1]
        else:
            # Disconnect last device in ring and connect predecessor to first device
            self.factory.devices[0].successor = None
            self.factory.devices.pop()

class RingFactory(protocol.Factory):
    def __init__(self):
        self.devices = []

    def buildProtocol(self, addr):
        return RingProtocol(self)

if __name__ == '__main__':
    factory = RingFactory()
    reactor.listenTCP(8000, factory)
    reactor.run()
