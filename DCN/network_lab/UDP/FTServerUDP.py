
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pickle

class EchoUDP(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        file_name, file_data = pickle.loads(datagram)
        print(f'{file_name} received!')
        file = open(file_name.rstrip('.txt') + 'Server.txt', 'a')
        file.write(file_data)
        file.close()
def main():
    reactor.listenUDP(1234, EchoUDP())
    reactor.run()

if __name__ == '__main__':
    main()
