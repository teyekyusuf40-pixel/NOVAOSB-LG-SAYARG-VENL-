import customtkinter as ctk
import os
import sys
import ctypes

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

class NovaStealthPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NovaOS - Ghost Protocol Elite")
        self.geometry("600x750")
        ctk.set_appearance_mode("dark")
        
        # Tasarım ve Başlık
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.main_frame, text="🛡️ GHOST PROTOCOL v4.0", font=("Orbitron", 26, "bold"), text_color="#00FF00")
        self.label.pack(pady=25)

        # 10 Ülke Listesi ve Proxy Adresleri
        self.proxies = {
            "Almanya (En Hızlı)": "88.99.10.251:1080",
            "Hollanda": "188.166.162.33:8080",
            "ABD - New York": "144.202.112.152:80",
            "İngiltere": "178.62.193.19:3128",
            "Fransa": "51.15.37.154:3128",
            "Japonya": "103.208.200.12:80",
            "Singapur": "139.59.105.151:8080",
            "Kanada": "158.69.53.111:3128",
            "İtalya": "185.241.208.204:80",
            "Brezilya": "18.228.198.150:80"
        }

        # Ülke Seçim Menüsü
        self.country_label = ctk.CTkLabel(self.main_frame, text="LOKASYON SEÇİN", font=("Arial", 14, "bold"))
        self.country_label.pack(pady=5)
        self.country_box = ctk.CTkOptionMenu(self.main_frame, values=list(self.proxies.keys()), fg_color="#1f538d", width=250)
        self.country_box.pack(pady=10)

        # Aktifleştirme Butonu
        self.activate_btn = ctk.CTkButton(self.main_frame, text="HAYALET MODUNU BAŞLAT", fg_color="#1b4d1b", 
                                        hover_color="#006400", command=self.start_ghost, height=50, font=("Arial", 16, "bold"))
        self.activate_btn.pack(pady=20, padx=60, fill="x")

        # Güvenlik Duvarı & Gizlilik Modülleri
        self.firewall_btn = self.create_module("SİSTEMİ DIŞARIYA KAPAT", self.toggle_firewall)
        self.dns_btn = self.create_module("İLENEMEZ DNS (Cloudflare)", self.toggle_dns)

        # Acil Durum & Temizlik
        self.reset_btn = ctk.CTkButton(self.main_frame, text="SİSTEMİ FABRİKA AYARINA DÖNDÜR", fg_color="#8B0000", 
                                      hover_color="#FF0000", command=self.emergency_reset, height=50)
        self.reset_btn.pack(pady=30, padx=60, fill="x")

        self.status_label = ctk.CTkLabel(self.main_frame, text="SİSTEM DURUMU: NORMAL", text_color="white")
        self.status_label.pack(side="bottom", pady=10)

        # Kapanışta Otomatik Sıfırlama
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_module(self, text, command):
        btn = ctk.CTkButton(self.main_frame, text=text + " [KAPALI]", fg_color="#333", command=lambda: command(btn))
        btn.pack(pady=10, padx=60, fill="x")
        btn.active = False
        return btn

    def start_ghost(self):
        choice = self.country_box.get()
        proxy_ip = self.proxies[choice]
        os.system(f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
        os.system(f'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "{proxy_ip}" /f')
        self.status_label.configure(text=f"AKTİF: {choice}", text_color="#00FF00")
        self.activate_btn.configure(text="BAĞLANTI AKTİF ✔", fg_color="#00FF00", text_color="black")

    def toggle_firewall(self, btn):
        btn.active = not btn.active
        if btn.active:
            os.system('netsh advfirewall firewall add rule name="NovaGuard" dir=out action=block')
            btn.configure(text="SİSTEM KAPALI ✔", fg_color="#1b4d1b")
        else:
            os.system('netsh advfirewall firewall delete rule name="NovaGuard"')
            btn.configure(text="SİSTEM AÇIK ✖", fg_color="#333")

    def toggle_dns(self, btn):
        btn.active = not btn.active
        if btn.active:
            os.system('netsh interface ip set dns "Wi-Fi" static 1.1.1.1')
            btn.configure(text="DNS: GİZLİ ✔", fg_color="#1b4d1b")
        else:
            os.system('netsh interface ip set dns "Wi-Fi" dhcp')
            btn.configure(text="DNS: NORMAL ✖", fg_color="#333")

    def emergency_reset(self):
        os.system('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f')
        os.system('netsh advfirewall firewall delete rule name="NovaGuard"')
        os.system('netsh interface ip set dns "Wi-Fi" dhcp')
        os.system('netsh int ip reset')
        self.status_label.configure(text="SİSTEM SIFIRLANDI", text_color="white")
        self.activate_btn.configure(text="HAYALET MODUNU BAŞLAT", fg_color="#1b4d1b", text_color="white")

    def on_closing(self):
        self.emergency_reset()
        self.destroy()

if __name__ == "__main__":
    if is_admin():
        app = NovaStealthPro()
        app.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)