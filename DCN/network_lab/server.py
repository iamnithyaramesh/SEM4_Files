from twisted.internet import reactor, protocol
import os

class FileReceiver(protocol.Protocol):
    def __init__(self):
        self.file_path = None
        self.file_handle = None
        self.file_name_received = False

    def connectionMade(self):
        print("Client connected.")

    def dataReceived(self, data):
        if not self.file_name_received:
            if data == b"READY":
                # The first message received is the filename
                self.file_name_received = True
                print("Client is ready to send file.")
                self.transport.write(b"SEND")
            else:
                print("Unexpected data received:", data)
                self.transport.loseConnection()
        else:
            # All subsequent data received is the file content
            self.writeToFile(data)

    

    def writeToFile(self, data):
        try:
            if self.file_path is None:
                # Haven't received filename yet, so ignore data
                return
            if self.file_handle is None:
                self.file_path='recieved.'+self.file_path.split('.')[1]
                print(self.file_path)
                self.file_handle = open(self.file_path, 'wb')
            self.file_handle.write(data)
        except Exception as e:
            print("Error writing to file:", e)
            self.transport.loseConnection()
        else:
            print(f"Received {len(data)} bytes")

    def connectionLost(self, reason):
        print("Connection lost with client.")
        if self.file_handle:
            self.file_handle.close()
            print(f"File '{self.file_path}' received and saved successfully!")

class FileTransferFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return FileReceiver()

def run_server():
    reactor.listenTCP(1234, FileTransferFactory())
    print("Server is listening on port 1234...")
    reactor.run()

if __name__ == "__main__":
    run_server()
