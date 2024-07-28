#from twisted.internet import reactor, protocol

#class SlidingWindowServer(protocol.Protocol):
#    def __init__(self):
#        self.window_size = 5
#        self.expected_seq_num = 0

#    def dataReceived(self, data):
#        seq_num, payload = self.parsePacket(data)
#        print(f"Received packet with seq_num: {seq_num}, payload: {payload}")
#        if seq_num == self.expected_seq_num:
#            print(f"Packet {seq_num} is in order, sending ACK.")
#            self.sendAck(seq_num)
#            self.expected_seq_num += 1
#        else:
#            print(f"Packet {seq_num} is out of order, expected {self.expected_seq_num}.")

#    def parsePacket(self, data):
#        parts = data.decode().split(':')
#        return int(parts[0]), parts[1]

#    def sendAck(self, seq_num):
#        ack_packet = f"ACK:{seq_num}".encode()
#        self.transport.write(ack_packet)

#class SlidingWindowFactory(protocol.Factory):
#    def buildProtocol(self, addr):
#        return SlidingWindowServer()

#reactor.listenTCP(8000, SlidingWindowFactory())
#reactor.run()

from twisted.internet import reactor, protocol

class SlidingWindowClient(protocol.Protocol):
    def __init__(self):
        self.window_size = 5
        self.base = 0
        self.next_seq_num = 0
        self.data = [str(i) for i in range(10)]  # Sample data to send
        self.acknowledged = set()

    def connectionMade(self):
        self.sendPackets()

    def dataReceived(self, data):
        ack_num = self.parseAck(data)
        print(f"Received ACK for packet: {ack_num}")
        self.acknowledged.add(ack_num)
        if ack_num == self.base:
            self.base += 1
            self.sendPackets()

    def parseAck(self, data):
        return int(data.decode().split(':')[1])

    def sendPackets(self):
        while self.next_seq_num < self.base + self.window_size and self.next_seq_num < len(self.data):
            if self.next_seq_num not in self.acknowledged:
                packet = f"{self.next_seq_num}:{self.data[self.next_seq_num]}"
                print(f"Sending packet: {packet}")
                self.transport.write(packet.encode())
            self.next_seq_num += 1

class SlidingWindowClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return SlidingWindowClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

reactor.connectTCP("localhost", 8000, SlidingWindowClientFactory())
reactor.run()
