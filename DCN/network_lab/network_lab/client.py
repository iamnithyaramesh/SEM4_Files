from twisted.internet import protocol, endpoints, reactor
import os

class FileSender(protocol.Protocol):
    def __init__(self, file_path):
        self.file_path = file_path

    def connectionMade(self):
        print("Connection established with the server.")
        self.transport.write(b"READY")

    def dataReceived(self, data):
        if data == b"SEND":
            print("Server is ready to receive file data.")
            self.sendFile()

    def sendFile(self):
        file_name = os.path.basename(self.file_path)
        print("Sending file:", file_name)
        try:
            with open(self.file_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.transport.write(data)
            print("File sent:", file_name)
        except Exception as e:
            print("Error sending file:", e)
            self.transport.loseConnection()

    def connectionLost(self, reason):
        print("Connection lost with the server.")

class FileTransferFactory(protocol.ClientFactory):
    def __init__(self, file_path):
        self.file_path = file_path

    def buildProtocol(self, addr):
        return FileSender(self.file_path)

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason)

def run_client(file_path):
    endpoint = endpoints.TCP4ClientEndpoint(reactor, "localhost", 1234)
    factory = FileTransferFactory(file_path)
    endpoint.connect(factory)
    reactor.run()

if __name__ == "__main__":
    file_path = "sample.jpg"
    run_client(file_path)
