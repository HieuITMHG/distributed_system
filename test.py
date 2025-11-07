import socket, struct, threading

MCAST_GRP = '239.255.0.1'
MCAST_PORT = 5007
LOCAL_IP = '192.168.1.4'  # ⚠️ Đổi thành IP của máy bạn (xem ipconfig)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Gắn socket vào cổng multicast
sock.bind(('', MCAST_PORT))

# Chỉ định card mạng cụ thể (interface)
mreq = struct.pack('4s4s', socket.inet_aton(MCAST_GRP), socket.inet_aton(LOCAL_IP))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Cho phép gửi/nhận trong cùng máy (loopback) và TTL đủ cao
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 5)

def receiver():
    while True:
        msg, addr = sock.recvfrom(1024)
        print(f"📩 {addr}: {msg.decode()}")

threading.Thread(target=receiver, daemon=True).start()

while True:
    data = input("Nhập tin: ")
    sock.sendto(data.encode(), (MCAST_GRP, MCAST_PORT))
