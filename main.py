import socket
import time
from datetime import datetime

interface_ip = '192.168.1.80'

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
sock.bind((interface_ip, 0))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    print("Listening for packets...")
    while True:
        packet, _ = sock.recvfrom(65535)
        ip_header = packet[14:34]
        src_ip = socket.inet_ntoa(ip_header[12:16])
        dst_ip = socket.inet_ntoa(ip_header[16:20])
        packet_size = len(packet)
        timestamp = datetime.now().strftime('%b %d %H:%M:%S')
        print(f"Timestamp: {timestamp}, Source IP: {src_ip}, Destination IP: {dst_ip}, Packet Size: {packet_size}")
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    sock.close()
