import socket
import struct
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

# --- Cấu hình multicast ---
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
BUFFER_SIZE = 1024

# --- Hàm nhận tin nhắn ---
def receive_messages(sock, text_area):
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            message = data.decode('utf-8')
            text_area.config(state=tk.NORMAL)
            text_area.insert(tk.END, f"{message}\n")
            text_area.config(state=tk.DISABLED)
            text_area.yview(tk.END)
        except Exception as e:
            print("Lỗi khi nhận:", e)
            break

# --- Hàm gửi tin nhắn ---
def send_message(event=None):
    msg = msg_entry.get()
    if msg:
        message = f"{username}: {msg}"
        sock.sendto(message.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
        msg_entry.delete(0, tk.END)

# --- Khởi tạo socket multicast ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# --- Tạo giao diện ---
root = tk.Tk()
root.title("Multicast Chat LAN")

username = simpledialog.askstring("Tên người dùng", "Nhập tên của bạn:", parent=root)
if not username:
    username = "Ẩn danh"

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
text_area.pack(padx=10, pady=10)

msg_entry = tk.Entry(root, width=40)
msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
msg_entry.bind("<Return>", send_message)

send_button = tk.Button(root, text="Gửi", command=send_message)
send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

# --- Thread nhận dữ liệu ---
thread = threading.Thread(target=receive_messages, args=(sock, text_area), daemon=True)
thread.start()

root.mainloop()
