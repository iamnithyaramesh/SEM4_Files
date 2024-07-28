

from __future__ import print_function

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver



class EchoClient(LineReceiver):
    end = b"Bye-bye!"

    def connectionMade(self):
        s=input("Enter the message: ")
        self.sendLine(s.encode())
        self.sendLine(self.end)


    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    def buildProtocol(self, addr) :

        return EchoClient() 


    # def clientConnectionFailed(self, connector, reason):
    #     print('connection failed:', reason.getErrorMessage())
    #     self.done.errback(reason)


    # def clientConnectionLost(self, connector, reason):
    #     print('connection lost:', reason.getErrorMessage())
    #     self.done.callback(None)



def main():
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 8000, factory)
    reactor.run()



if __name__ == '__main__':
    main()
