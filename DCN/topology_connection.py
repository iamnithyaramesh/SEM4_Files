from twisted.internet import reactor, protocol

class Node(protocol.Protocol):
    def __init__(self, node_id):
        self.node_id = node_id

    def connectionMade(self):
        print("Node {} connected".format(self.node_id))

    def dataReceived(self, data):
        print("Node {} received: {}".format(self.node_id, data.decode()))

    def sendMessage(self, message):
        self.transport.write(message.encode())

class NetworkTopology:
    def __init__(self):
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)

    def connectNodes(self):
        pass  

class BusTopology(NetworkTopology):
    def connectNodes(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].transport.connect(self.nodes[i + 1].transport)

class StarTopology(NetworkTopology):
    def connectNodes(self):
        for node in self.nodes[1:]:
            self.nodes[0].transport.connect(node.transport)

class RingTopology(NetworkTopology):
    def connectNodes(self):
        for i in range(len(self.nodes)):
            self.nodes[i].transport.connect(self.nodes[(i + 1) % len(self.nodes)].transport)

class MeshTopology(NetworkTopology):
    def connectNodes(self):
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                self.nodes[i].transport.connect(self.nodes[j].transport)

def createNodes(topology, num_nodes):
    nodes = []
    for i in range(num_nodes):
        node = Node(i)
        factory = protocol.ClientFactory()
        factory.protocol = lambda: node
        reactor.connectTCP('localhost', 8000, factory)
        nodes.append(node)
        topology.addNode(node)
    return nodes

def simulate(topology):
    topology.connectNodes()
    reactor.run()

if __name__ == "__main__":
    # Example usage:
    num_nodes = 5

    # Bus Topology
    bus_topology = BusTopology()
    bus_nodes = createNodes(bus_topology, num_nodes)
    simulate(bus_topology)

    # Star Topology
    star_topology = StarTopology()
    star_nodes = createNodes(star_topology, num_nodes)
    simulate(star_topology)

    # Ring Topology
    ring_topology = RingTopology()
    ring_nodes = createNodes(ring_topology, num_nodes)
    simulate(ring_topology)

    # Mesh Topology
    mesh_topology = MeshTopology()
    mesh_nodes = createNodes(mesh_topology, num_nodes)
    simulate(mesh_topology)
