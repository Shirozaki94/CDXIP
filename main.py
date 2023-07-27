import socket
import time
from datetime import datetime
from openpyxl import Workbook

interface_ip = '192.168.1.80'
port = 443
output_file = 'packet_log.xlsx'
workbook = Workbook()
sheet = workbook.active
sheet.append(['Timestamp', 'Source IP', 'Destination IP', 'Packet Size'])
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
sock.bind((interface_ip, 0))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
while True:
    try:
        packet, _ = sock.recvfrom(65535)
        ip_header = packet[14:34]
        src_ip = socket.inet_ntoa(ip_header[12:16])
        dst_ip = socket.inet_ntoa(ip_header[16:20])
        packet_size = len(packet)
        timestamp = datetime.now().strftime('%b %d %H:%M:%S')
        sheet.append([timestamp, src_ip, dst_ip, packet_size])
        workbook.save(output_file)
        time.sleep(1)
    except KeyboardInterrupt:
        break
sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
sock.close()
