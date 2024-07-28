\
from twisted.internet import reactor, protocol

class StopAndWaitServer(protocol.Protocol): 
    def connectionMade(self):
        print("Client connected:", self.transport.getPeer()) 
        self.send_message()

def send_message(self):
    message = input("Enter message: ") 
    self.transport.write(message.encode()) 
    print("Message sent to client:", message) 
    self.expected_ack = "ACK" #self.schedule_resend()

def schedule_resend(self):
    self.resend_call = reactor.callLater(5, self.resend_message)

def resend_message(self):
    print("ACK not received. Resending message...") 
    self.send_message()

def dataReceived(self, data): 
    ack = data.decode() 
    print("ACK received:", ack) 
    if ack == self.expected_ack:
#self.resend_call.cancel()
        print("ACK received. Message acknowledged.") 
        self.send_message()
    else:
        print("Invalid ACK received.") 
        self.schedule_resend()

def connectionLost(self, reason): print("Client disconnected:")

class StopAndWaitServerFactory(protocol.Factory): def buildProtocol(self, addr):
return StopAndWaitServer() server_port = 8000
factory = StopAndWaitServerFactory() reactor.listenTCP(server_port, factory)

reactor.run() 
#Client
from twisted.internet import reactor, protocol class StopAndWaitClient(protocol.Protocol):
def connectionMade(self): print("Connected to server.") self.send_ack()

def send_ack(self):
self.transport.write(input("Enter ack: ").encode()) print("ACK sent")

def dataReceived(self, data): message = data.decode()
print("Message received:", message) self.send_ack()

def connectionLost(self, reason):
print("Connection lost:", reason.getErrorMessage())

class StopAndWaitClientFactory(protocol.ClientFactory): def buildProtocol(self, addr):
return StopAndWaitClient()

def clientConnectionFailed(self, connector, reason): print("Connection failed:", reason.getErrorMessage()) reactor.stop()

def clientConnectionLost(self, connector, reason): print("Connection lost:", reason.getErrorMessage()) reactor.stop()

server_address = 'localhost' server_port = 8000

factory = StopAndWaitClientFactory() reactor.connectTCP(server_address, server_port, factory) reactor.run()