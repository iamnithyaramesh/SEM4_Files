from twisted.internet import reactor, protocol

class RPCServerProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Client connected")

    def dataReceived(self, data):
        commands = data.decode().splitlines()
        for command in commands:
            result = self.handleCommand(command)
            self.transport.write(result.encode() + b'\n')

    def handleCommand(self, command):
        parts = command.split(' ')
        if parts[0] == "add":
            return str(self.add(int(parts[1]), int(parts[2])))
        elif parts[0] == "multiply":
            return str(self.multiply(int(parts[1]), int(parts[2])))
        else:
            return "Unknown command"

    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

class RPCServerFactory(protocol.ServerFactory):
    protocol = RPCServerProtocol

reactor.listenTCP(1234, RPCServerFactory())
reactor.run()



#from twisted.internet import reactor, protocol

#class RPCClientProtocol(protocol.Protocol):
#    def connectionMade(self):
#        self.sendCommand("add 2 3")
#        self.sendCommand("multiply 4 5")
#        self.transport.loseConnection()

#    def sendCommand(self, command):
#        self.transport.write(command.encode() + b'\n')

#    def dataReceived(self, data):
#        print("Result:", data.decode().strip())

#class RPCClientFactory(protocol.ClientFactory):
#    protocol = RPCClientProtocol

#    def clientConnectionFailed(self, connector, reason):
#        print("Connection failed:", reason.getErrorMessage())
#        reactor.stop()

#reactor.connectTCP("localhost", 1234, RPCClientFactory())
#reactor.run()
