import tkinter as tk
from tkinter import messagebox
import random
import requests

API_URL = "http://127.0.0.1:8585"

# ПАЛИТРА CASHVPN (Матовые тёмно-зелёные тона денег)
CASH_GREEN = "#00E666"        # Яркий неоновый зелёный
DARK_EMERALD = "#050F08"      # Фон приложения
CARD_BG = "#0D260F"           # Тёмно-зелёный для кнопок серверов
TEXT_WHITE = "#F2FFF5"     
TEXT_MUTED = "#59A673"     
CASH_RED = "#E61A33"          # Красный цвет кнопки (Отключено)

class VPNAppTk:
    def __init__(self, root):
        self.root = root
        self.root.title("CashVPN")
        self.root.geometry("380x650")
        self.root.resizable(False, False)
        self.root.configure(bg=DARK_EMERALD)
        
        self.current_server_ip = "46.165.2.11"
        self.is_connected = False
        self.time_elapsed = 0
        self.servers_list = [
            {"name": "Germany (Frankfurt)", "ping": "Online", "ip": "46.165.2.11"},
            {"name": "USA (New York)", "ping": "Online", "ip": "8.8.8.8"},
            {"name": "Netherlands (Amsterdam)", "ping": "Online", "ip": "185.200.118.4"}
        ]
        
        # Контейнер для экранов
        self.main_frame = tk.Frame(self.root, bg=DARK_EMERALD)
        self.menu_frame = tk.Frame(self.root, bg=DARK_EMERALD)
        self.server_frame = tk.Frame(self.root, bg=DARK_EMERALD)
        
        # Запуск экрана загрузки, затем главного
        self.show_splash()

    def show_splash(self):
        """Экран загрузки с анимацией"""
        self.splash_frame = tk.Frame(self.root, bg=DARK_EMERALD)
        self.splash_frame.pack(fill="both", expand=True)
        
        self.money_label = tk.Label(self.splash_frame, text="[ CASH ]", font=("Arial", 36, "bold"), fg=CASH_GREEN, bg=DARK_EMERALD)
        self.money_label.pack(pady=(150, 20))
        
        tk.Label(self.splash_frame, text="CashVPN", font=("Arial", 28, "bold"), fg=CASH_GREEN, bg=DARK_EMERALD).pack()
        self.status_label = tk.Label(self.splash_frame, text="Загрузка приложения...", font=("Arial", 12), fg=TEXT_MUTED, bg=DARK_EMERALD)
        self.status_label.pack(pady=20)
        
        self.frames = ["$  ", " $$ ", "  $$$", " $$$$", " $$$$$"]
        self.frame_idx = 0
        self.counter = 0
        self.animate_splash()

    def animate_splash(self):
        self.money_label.configure(text=f"[ {self.frames[self.frame_idx]} ]")
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.counter += 1
        
        if self.counter == 12:
            self.status_label.configure(text="Шифрование каналов...")
        
        if self.counter >= 25:
            self.splash_frame.pack_forget()
            self.build_main_screen()
            self.build_menu_screen()
            self.build_server_screen()
            self.show_screen(self.main_frame)
            # Безопасный запрос к API сервера
            self.root.after(500, self.load_servers_from_api)
        else:
            self.root.after(100, self.animate_splash)

    def build_main_screen(self):
        """Главный экран"""
        self.main_frame.pack(fill="both", expand=True)
        
        # Хедер
        header = tk.Frame(self.main_frame, bg=DARK_EMERALD, height=50)
        header.pack(fill="x", pady=10)
        
        menu_btn = tk.Button(header, text="☰ Menu", font=("Arial", 12, "bold"), fg=CASH_GREEN, bg=DARK_EMERALD, bd=0, activebackground=DARK_EMERALD, command=lambda: self.show_screen(self.menu_frame))
        menu_btn.pack(side="left", padx=15)
        
        tk.Label(header, text="CashVPN", font=("Arial", 18, "bold"), fg=CASH_GREEN, bg=DARK_EMERALD).pack(side="left", padx=40)
        
        # Центральная кнопка подключения
        self.connect_btn = tk.Button(self.main_frame, text="CONNECT", font=("Arial", 18, "bold"), fg=TEXT_WHITE, bg=CASH_RED, width=14, height=5, bd=0, command=self.toggle_connection)
        self.connect_btn.pack(pady=40)
        
        # Статистика
        self.speed_lbl = tk.Label(self.main_frame, text="Speed: 0 Kb/s", font=("Arial", 13), fg=TEXT_WHITE, bg=DARK_EMERALD)
        self.speed_lbl.pack(pady=5)
        
        self.time_lbl = tk.Label(self.main_frame, text="Time: 00:00:00", font=("Arial", 12), fg=TEXT_MUTED, bg=DARK_EMERALD)
        self.time_lbl.pack(pady=5)
        
        self.ip_lbl = tk.Label(self.main_frame, text="IP: 192.168.1.104 (Protected: NO)", font=("Arial", 11), fg=TEXT_MUTED, bg=DARK_EMERALD)
        self.ip_lbl.pack(pady=5)
        
        # Нижняя плажка выбора сервера
        self.server_bar = tk.Button(self.main_frame, text="Germany (Frankfurt)  |  Online", font=("Arial", 12, "bold"), fg=TEXT_WHITE, bg=CARD_BG, bd=1, relief="solid", highlightcolor=CASH_GREEN, height=2, command=lambda: self.show_screen(self.server_frame))
        self.server_bar.pack(fill="x", side="bottom", padx=20, pady=30)

    def build_menu_screen(self):
        """Экран настроек"""
        tk.Label(self.menu_frame, text="Settings Menu", font=("Arial", 20, "bold"), fg=CASH_GREEN, bg=DARK_EMERALD).pack(pady=30)
        
        menu_items = ["⚙ Настройки", "⭐ Оценить нас", "❓ Помощь", "✉ Обратная связь", "🔗 Поделиться"]
        for name in menu_items:
            tk.Button(self.menu_frame, text=name, font=("Arial", 13, "bold"), fg=TEXT_WHITE, bg=CARD_BG, bd=0, height=2, width=25, command=lambda n=name: print(f"Клик: {n}")).pack(pady=8)
            
        tk.Button(self.menu_frame, text="Back", font=("Arial", 12, "bold"), fg=CASH_GREEN, bg="#1a1a1a", bd=0, height=2, width=15, command=lambda: self.show_screen(self.main_frame)).pack(side="bottom", pady=40)

    def build_server_screen(self):
        """Экран выбора серверов"""
        self.server_container = tk.Frame(self.server_frame, bg=DARK_EMERALD)
        self.server_container.pack(fill="both", expand=True)
        self.refresh_servers_ui()

    def refresh_servers_ui(self):
        for widget in self.server_container.winfo_children():
            widget.destroy()
            
        tk.Label(self.server_container, text="Select Location", font=("Arial", 20, "bold"), fg=CASH_GREEN, bg=DARK_EMERALD).pack(pady=30)
        
        for data in self.servers_list:
            btn_text = f"{data['name']} [{data['ping']}]\nIP: {data['ip']}"
            btn = tk.Button(self.server_container, text=btn_text, font=("Arial", 12, "bold"), fg=TEXT_WHITE, bg=CARD_BG, bd=0, height=3, width=28, command=lambda d=data: self.select_server(d))
            btn.pack(pady=10)
            
        tk.Button(self.server_container, text="Back", font=("Arial", 12, "bold"), fg=CASH_GREEN, bg="#1a1a1a", bd=0, height=2, width=15, command=lambda: self.show_screen(self.main_frame)).pack(side="bottom", pady=40)

    def load_servers_from_api(self):
        try:
            response = requests.get(f"{API_URL}/servers", timeout=2)
            if response.status_code == 200:
                self.servers_list = response.json()
                self.refresh_servers_ui()
        except Exception:
            pass

    def select_server(self, data):
        self.current_server_ip = data["ip"]
        self.server_bar.configure(text=f"{data['name']}  |  {data['ping']}")
        if self.is_connected:
            self.ip_lbl.configure(text=f"IP: {data['ip']} (Protected: YES)")
        self.show_screen(self.main_frame)

    def toggle_connection(self):
        self.is_connected = not self.is_connected
        if self.is_connected:
            self.connect_btn.configure(text="PROTECTED", bg=CASH_GREEN, fg=DARK_EMERALD)
            self.ip_lbl.configure(text=f"IP: {self.current_server_ip} (Protected: YES)", fg=CASH_GREEN)
            self.time_elapsed = 0
            self.update_timer_loop()
        else:
            self.connect_btn.configure(text="CONNECT", bg=CASH_RED, fg=TEXT_WHITE)
            self.ip_lbl.configure(text="IP: 192.168.1.104 (Protected: NO)", fg=TEXT_MUTED)
            self.speed_lbl.configure(text="Speed: 0 Kb/s")

    def update_timer_loop(self):
        if self.is_connected:
            self.time_elapsed += 1
            hours = self.time_elapsed // 3600
            minutes = (self.time_elapsed % 3600) // 60
            seconds = self.time_elapsed % 60
            self.time_lbl.configure(text=f"Time: {hours:02}:{minutes:02}:{seconds:02}")
            self.speed_lbl.configure(text=f"Speed: {random.randint(450, 1200)} Kb/s")
            self.root.after(1000, self.update_timer_loop)

    def show_screen(self, frame):
        self.main_frame.pack_forget()
        self.menu_frame.pack_forget()
        self.server_frame.pack_forget()
        frame.pack(fill="both", expand=True)

if __name__ == '__main__':
    root = tk.Tk()
    app = VPNAppTk(root)
    root.mainloop()
