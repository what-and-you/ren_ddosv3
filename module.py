# module.py

import requests
import dns.resolver

# Fungsi untuk memeriksa status website
def cek_status_website(url):
    try:
        response = requests.get(url, timeout=10)
        return response
    except requests.RequestException as e:
        print(f"Error saat mengakses {url}: {e}")
        return None

# Fungsi untuk memeriksa SSL/TLS pada website
def cek_ssl_website(url):
    try:
        if url.startswith("https"):
            return "TLS 1.3 (simulasi)"
        else:
            return None
    except Exception as e:
        print(f"Error saat mengecek SSL: {e}")
        return None

# Fungsi untuk memeriksa DNS record dari sebuah domain
def cek_dns(url):
    try:
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]
        answers = dns.resolver.resolve(domain, "A")
        return [str(rdata) for rdata in answers]
    except Exception as e:
        print(f"Error saat mengecek DNS: {e}")
        return None

# Fungsi untuk memeriksa apakah website menggunakan HSTS
def cek_hsts(response):
    try:
        return response.headers.get("Strict-Transport-Security", None)
    except Exception as e:
        print(f"Error saat mengecek HSTS: {e}")
        return None

# Fungsi untuk memeriksa CORS (Cross-Origin Resource Sharing)
def cek_cors(response):
    try:
        return response.headers.get("Access-Control-Allow-Origin", None)
    except Exception as e:
        print(f"Error saat mengecek CORS: {e}")
        return None
