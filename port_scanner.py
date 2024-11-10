#!/usr/bin/env python3
import socket
import re
import threading

# Regular expression untuk memvalidasi IPv4 address
ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
# Regular expression untuk memvalidasi range port
port_range_pattern = re.compile(r"([0-9]+)-([0-9]+)")

# Variabel untuk menyimpan rentang port
port_min = 0
port_max = 65535

# Daftar untuk menyimpan port yang terbuka
open_ports = []

# Fungsi untuk memindai port tertentu
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))  # Menggunakan connect_ex untuk menghindari error yang bisa terjadi
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "Unknown Service"
                open_ports.append((port, service))
    except Exception as e:
        pass

# Fungsi utama untuk memulai pemindaian
def port_scanner(ip, port_min, port_max):
    threads = []
    for port in range(port_min, port_max + 1):
        # Membuat thread untuk setiap pemindaian port
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    
    # Menunggu semua thread selesai
    for t in threads:
        t.join()

    # Menampilkan hasil
    if open_ports:
        print(f"\nHasil pemindaian pada {ip}:")
        for port, service in open_ports:
            print(f"Port {port} terbuka: Layanan {service}")
    else:
        print(f"Tidak ada port terbuka yang ditemukan pada {ip}.")


# Input alamat IP dari user
while True:
    ip_add_entered = input("\nMasukkan alamat IP yang ingin dipindai: ")
    if ip_add_pattern.search(ip_add_entered):
        print(f"{ip_add_entered} adalah alamat IP yang valid")
        break

# Input rentang port dari user
while True:
    print("Masukkan rentang port yang ingin dipindai dalam format <int>-<int> (contoh: 60-120)")
    port_range = input("Masukkan rentang port: ")
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break

# Memulai pemindaian
print(f"Memulai pemindaian pada {ip_add_entered} dari port {port_min} hingga {port_max}...")
port_scanner(ip_add_entered, port_min, port_max)
