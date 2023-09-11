import socket
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation

# Set the style for the plots
sns.set_style("whitegrid")
interface_ip = '192.168.1.80'

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
sock.bind((interface_ip, 0))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

packet_sizes = []  # List to store packet sizes
timestamps = []  # List to store timestamps

# Create subplots for the histogram and timeline
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))


def update_plot(i):
    packet, _ = sock.recvfrom(65535)
    ip_header = packet[14:34]
    src_ip = socket.inet_ntoa(ip_header[12:16])
    dst_ip = socket.inet_ntoa(ip_header[16:20])
    packet_size = len(packet)
    timestamp = datetime.now().strftime('%b %d %H:%M:%S')
    print(f"Timestamp: {timestamp}, Source IP: {src_ip}, Destination IP: {dst_ip}, Packet Size: {packet_size}")

    # Append packet size and timestamp to lists
    packet_sizes.append(packet_size)
    timestamps.append(datetime.now())

    # Update histogram
    ax1.clear()
    sns.histplot(packet_sizes, bins=20, ax=ax1, color='blue', kde=True)
    ax1.set_title("Histogram of Packet Sizes")
    ax1.set_xlabel("Packet Size")
    ax1.set_ylabel("Frequency")

    # Update timeline
    ax2.clear()
    ax2.plot(timestamps, range(len(timestamps)), marker='o', color='green')
    ax2.set_title("Timeline of Packet Arrivals")
    ax2.set_xlabel("Timestamp")
    ax2.set_ylabel("Packet Index")


ani = FuncAnimation(fig, update_plot, interval=1000)

try:
    print("Listening for packets...")
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    sock.close()
