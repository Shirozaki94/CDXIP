import socket
import time
from datetime import datetime
from openpyxl import Workbook

# Set the network interface IP address to capture packets from
interface_ip = '192.168.1.80'  # Replace with your network interface IP address

# Set the port number to filter packets
port = 443  # Replace with the desired port number

# Set the output file name
output_file = 'packet_log.xlsx'  # Replace with your desired output file name

# Create a new workbook and get the active sheet
workbook = Workbook()
sheet = workbook.active

# Set the headers in the first row of the sheet
sheet.append(['Timestamp', 'Source IP', 'Destination IP', 'Packet Size'])

# Create a raw socket to capture packets
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
sock.bind((interface_ip, 0))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# Capture and write packets every second until interrupted
while True:
    try:
        # Receive a packet
        packet, _ = sock.recvfrom(65535)

        # Extract the IP header from the packet
        ip_header = packet[14:34]

        # Unpack the IP header to get the source and destination IP addresses
        src_ip = socket.inet_ntoa(ip_header[12:16])
        dst_ip = socket.inet_ntoa(ip_header[16:20])

        # Extract the packet size
        packet_size = len(packet)

        # Get the current timestamp
        timestamp = datetime.now().strftime('%b %d %H:%M:%S')

        # Add the log entry to the sheet
        sheet.append([timestamp, src_ip, dst_ip, packet_size])

        # Save the workbook
        workbook.save(output_file)

        # Wait for 1 second before capturing the next packet
        time.sleep(1)

    except KeyboardInterrupt:
        break

# Disable promiscuous mode and close the socket
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
sock.close()
