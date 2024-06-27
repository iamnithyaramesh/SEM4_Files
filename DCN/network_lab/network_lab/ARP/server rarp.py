"""from twisted.internet import reactor, protocol
import struct

class RARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")
 
    def dataReceived(self, data):
        global rarp_tabel
        rec=eval(data.decode())
        ip_address='0.0.0.0'
        # get_parts=data.split()
        rarp_packet_format="!6s4s6s4s"
        rarp_data=struct.unpack(rarp_packet_format,rec.get('req_format')) #unpacking the format
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = rarp_data
        
        print("Received RARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if rec.get('req')=="RARP_REQUEST":
            for i in rarp_tabel:
                if i==rec.get('mac'):
                    ip_address=rarp_tabel[i]
                else:
                    continue 
            l=[]
            for i in ip_address.split('.'):
                l.append(int(i)) #list contains ip address

            mac_address =rec.get('mac') # Example MAC address
            response_packet = struct.pack( #packing the data to client now source and destination are swapped
            rarp_packet_format,
            Target_Hardware_Address,
            Target_Protocol_Address,
            Source_Hardware_Address,
            bytes(l),
            
        )
            to_client={'reply_format':response_packet} # dict to differntiate reply format and ip addres to be sent
            if ip_address !='0.0.0.0':
                rarp_reply = f'RARP_REPLY {mac_address} {ip_address}\n'
                
                to_client['data']=rarp_reply
                self.transport.write(str(to_client).encode()) # encoded data is send
                print("IP Address sent")
                
            else:
                self.transport.write(b'hi')
                print("invalid MAC recieved ")
                
    def connectionLost(self, reason):
        print("client removed")
        return
    
class RARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RARPServer()

rarp_tabel={}
rarp_tabel['00:11:22:33:44:55']='192.168.1.1'
reactor.listenTCP(1230, RARPServerFactory())
reactor.run()
"""

from twisted.internet import reactor, protocol
import struct

class RARPServer(protocol.Protocol):
    def connectionMade(self):
        print("Client connected")
        self.factory.clients.append(self)
        self.client_mac = None

    def dataReceived(self, data):
        global rarp_table
        rec = eval(data.decode())
        ip_address = '0.0.0.0'

        rarp_packet_format = "!6s4s6s4s"
        rarp_data = struct.unpack(rarp_packet_format, rec.get('req_format'))  # Unpacking the format
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = rarp_data
        
        print("Received RARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if rec.get('req') == "RARP_REQUEST":
            self.client_mac = rec.get('mac')  # Store the MAC address requested by the client

            ip_address = rarp_table.get(self.client_mac, '0.0.0.0')  # Look up IP address for the requested MAC

            l = []
            for i in ip_address.split('.'):
                l.append(int(i))  # List contains IP address bytes

            response_packet = struct.pack(  # Packing the data to client now source and destination are swapped
                rarp_packet_format,
                Target_Hardware_Address,
                Target_Protocol_Address,
                Source_Hardware_Address,
                bytes(l),
            )
            to_client = {'reply_format': response_packet}  # Dict to differentiate reply format and IP address to be sent
            if ip_address != '0.0.0.0':
                rarp_reply = f'RARP_REPLY {self.client_mac} {ip_address}\n'
                to_client['data'] = rarp_reply
                data_to_send = str(to_client).encode()

                # Send response to the requesting client only
                self.transport.write(data_to_send)
                print("IP Address sent")
            else:
                self.transport.write(b'hi')
                print("Invalid MAC received")

    def connectionLost(self, reason):
        print("Client removed")
        self.factory.clients.remove(self)
        if self.client_mac in rarp_table:
            del rarp_table[self.client_mac]  # Remove the client's MAC from the RARP table if it exists

class RARPServerFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        protocol_instance = RARPServer()
        protocol_instance.factory = self  # Set the factory attribute of the protocol instance
        return protocol_instance

rarp_table = {
    '00:11:22:33:44:55': '192.168.1.1',
    '00:55:66:77:88:99': '192.168.1.2',
    '11:22:33:44:55:66': '192.168.1.3',
    '22:33:44:55:66:77': '192.168.1.4',
    '33:44:55:66:77:88': '192.168.1.5'
}

reactor.listenTCP(1230, RARPServerFactory())
reactor.run()



