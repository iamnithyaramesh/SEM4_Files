
from twisted.internet import reactor, protocol
import struct

class ARPServer(protocol.Protocol):
    def connectionMade(self):
        print("Client connected")
        self.factory.clients.append(self)
        self.client_ip = None

    def dataReceived(self, data):
        global arp_table
        rec = eval(data.decode())
        mac_address = '0:0:0:0:0:0'

        arp_packet_format = "!6s4s6s4s"
        arp_data = struct.unpack(arp_packet_format, rec.get('req_format'))  # Unpacking the format
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = arp_data

        print("Received ARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))

        if rec.get('req') == "ARP_REQUEST":
            self.client_ip = rec.get('ip')  # Store the IP address requested by the client

            mac_address = arp_table.get(self.client_ip, '0:0:0:0:0:0')  # Look up MAC address for the requested IP

            l = []
            for i in mac_address.split(':'):
                l.append(int(i))  # list contains MAC address

            ip_address = self.client_ip  # Example IP address
            response_packet = struct.pack(  # Packing the data to client now source and destination are swapped
                arp_packet_format,
                Target_Hardware_Address,
                Target_Protocol_Address,
                Source_Hardware_Address,
                bytes(l),
            )
            to_client = {'reply_format': response_packet}  # dict to differentiate reply format and ip address to be sent
            if mac_address != '0:0:0:0:0:0':
                arp_reply = f'ARP_REPLY {ip_address} {mac_address}\n'
                to_client['data'] = arp_reply
                data_to_send = str(to_client).encode()

                # Send response to the requesting client only
                self.transport.write(data_to_send)

                print("MAC Address sent")
            else:
                self.transport.write(b'hi')
                print("Invalid IP received")

    def connectionLost(self, reason):
        print("Client removed")
        self.factory.clients.remove(self)
        if self.client_ip in arp_table:
            del arp_table[self.client_ip]  # Remove the client's IP from the ARP table if it exists

class ARPServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        protocol_instance = ARPServer()
        protocol_instance.factory = self  # Set the factory attribute of the protocol instance
        return protocol_instance

arp_table = {
    '192.168.1.1': '00:11:22:33:44:55',
    '192.168.1.2': '00:55:66:77:88:99',
    '192.168.1.3': '11:22:33:44:55:66',
    '192.168.1.4': '22:33:44:55:66:77',
    '192.168.1.5': '33:44:55:66:77:88'
}

reactor.listenTCP(1234, ARPServerFactory())
reactor.run()
