import pyshark
import pandas as pd
import matplotlib.pyplot as plt

def capture_packets(interface, count=100):
    print(f"Capturing {count} packets from interface {interface}...")
    capture = pyshark.LiveCapture(interface=interface)
    packets = []
    packets_captured=0
    for packet in capture.sniff_continuously(packet_count=count):
        packets.append(packet)
        packets_captured += 1
        print(f"Packets captured: {packets_captured}/{count}")

    return packets


def analyze_packet(packet):
    try:
        packet_info = {'packet_size': int(packet.length)}

        # Check if the packet has an IP layer
        if hasattr(packet, 'ip'):
            packet_info.update({
                'src_ip': packet.ip.src,
                'dst_ip': packet.ip.dst
            })

            if 'TCP' in packet:
                packet_info.update({
                    'protocol': 'TCP',
                    'src_port': packet.tcp.srcport,
                    'dst_port': packet.tcp.dstport
                })
                if packet.tcp.srcport == '21' or packet.tcp.dstport == '21':
                    packet_info['protocol'] = 'FTP'
                elif packet.tcp.srcport == '25' or packet.tcp.dstport == '25':
                    packet_info['protocol'] = 'SMTP'
            elif 'UDP' in packet:
                packet_info.update({
                    'protocol': 'UDP',
                    'src_port': packet.udp.srcport,
                    'dst_port': packet.udp.dstport
                })
            elif 'IGMP' in packet:
                packet_info.update({
                    'protocol': 'IGMP'
                })
            elif 'ICMP' in packet:
                packet_info.update({
                    'protocol': 'ICMP'
                })
            else:
                packet_info.update({
                    'protocol': 'Other IP'
                })
        elif hasattr(packet, 'arp'):
            packet_info.update({
                'protocol': 'ARP',
                'src_ip': packet.arp.src_proto_ipv4,
                'dst_ip': packet.arp.dst_proto_ipv4
            })
        elif hasattr(packet, 'rarp'):
            packet_info.update({
                'protocol': 'RARP'
            })
        elif hasattr(packet, 'dns'):
            packet_info.update({
                'protocol': 'DNS'
            })
        elif hasattr(packet, 'dhcp'):
            packet_info.update({
                'protocol': 'DHCP'
            })
        
        elif hasattr(packet, 'http'):
            packet_info.update({
                'protocol': 'HTTP'
            })
        
        else:
            pass
        print(f"Packet: {packet_info}")
        return packet_info
    except Exception as e:
        print(f"Error analyzing packet: {e}")
        return None

def visualize_packet_size_distribution(data):
    try:
        packet_sizes = [packet['packet_size'] for packet in data if packet]
        if not packet_sizes:
            print("No valid packet sizes to display.")
            return

        plt.figure(figsize=(10, 6))
        plt.hist(packet_sizes, bins=20, color='skyblue', edgecolor='black')
        plt.title('Packet Size Distribution')
        plt.xlabel('Packet Size (bytes)')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error visualizing packet size distribution: {e}")

def visualize_traffic_by_protocol(data):
    try:
        df = pd.DataFrame([packet for packet in data if packet])
        if df.empty:
            print("No valid packet data to display.")
            return

        protocol_counts = df['protocol'].value_counts()

        plt.figure(figsize=(8, 6))
        protocol_counts.plot(kind='bar', color='salmon')
        plt.title('Traffic by Protocol')
        plt.xlabel('Protocol')
        plt.ylabel('Packet Count')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error visualizing traffic by protocol: {e}")

def main():
    interface = 'Wi-Fi'  # Update with your network interface
    packet_count = 1000

    # Capture packets
    packets = capture_packets(interface, count=packet_count)

    # Analyze packets
    decoded_packets = [analyze_packet(packet) for packet in packets]

    # Visualize packet size distribution
    visualize_packet_size_distribution(decoded_packets)

    # Visualize traffic by protocol
    visualize_traffic_by_protocol(decoded_packets)

if __name__ == '__main__':
    main()
