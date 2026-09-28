import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

# --- Цвета ---
CASH_GREEN = (0/255, 230/255, 102/255, 1)
DARK_EMERALD = (5/255, 15/255, 8/255, 1)
CARD_BG = (13/255, 38/255, 15/255, 1)
TEXT_WHITE = (242/255, 255/255, 245/255, 1)
TEXT_MUTED = (89/255, 166/255, 115/255, 1)
CASH_RED = (230/255, 26/255, 51/255, 1)

class ServerButton(Button):
    def __init__(self, server_data, callback, **kwargs):
        super().__init__(**kwargs)
        self.server = server_data
        self.callback = callback
        self.text = f"{server_data['name']}\n{server_data['ip']}"
        self.background_color = CARD_BG
        self.color = TEXT_WHITE
        self.size_hint_y = None
        self.height = 60
        self.bind(on_press=self.on_select)

    def on_select(self, instance):
        self.callback(self.server)

class CashVPNApp(App):
    def build(self):
        Window.clearcolor = DARK_EMERALD
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="[ CASH ] CashVPN", font_size=28, color=CASH_GREEN, size_hint=(1, 0.15), bold=True, markup=True)
        main_layout.add_widget(title)

        card = BoxLayout(orientation='vertical', size_hint=(1, 0.6), padding=10, spacing=10)
        self.connect_btn = Button(text="CONNECT", font_size=24, bold=True, size_hint=(1, 0.3), background_color=CASH_RED, color=(1,1,1,1))
        self.connect_btn.bind(on_press=self.toggle_connection)
        card.add_widget(self.connect_btn)

        stats_layout = BoxLayout(size_hint=(1, 0.7), orientation='vertical')
        self.ip_label = Label(text="IP: 192.168.1.1", color=TEXT_MUTED, font_size=16)
        self.time_label = Label(text="Time: 00:00:00", color=TEXT_WHITE, font_size=18, bold=True)
        self.speed_label = Label(text="Speed: 0 Kb/s", color=TEXT_MUTED, font_size=14)
        stats_layout.add_widget(self.ip_label)
        stats_layout.add_widget(self.time_label)
        stats_layout.add_widget(self.speed_label)
        card.add_widget(stats_layout)
        main_layout.add_widget(card)

        servers_container = BoxLayout(size_hint=(1, 0.25), padding=5)
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.25))
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        self.servers_list = [
            {"name": "Germany (Frankfurt)", "ip": "46.165.2.11"},
            {"name": "USA (New York)", "ip": "8.8.8.8"},
            {"name": "Netherlands (Amsterdam)", "ip": "185.200.118.4"},
            {"name": "France (Paris)", "ip": "1.1.1.1"},
            {"name": "Japan (Tokyo)", "ip": "203.0.113.1"},
        ]
        self.current_server = self.servers_list

        for srv in self.servers_list:
            btn = ServerButton(srv, self.select_server)
            btn.size_hint_y = None
            btn.height = 60
            grid.add_widget(btn)
        scroll.add_widget(grid)
        servers_container.add_widget(scroll)
        main_layout.add_widget(servers_container)

        self.is_connected = False
        self.start_time = 0
        return main_layout

    def select_server(self, server):
        self.current_server = server
        self.ip_label.text = f"IP: {server['ip']}"
        if self.is_connected:
            self.ip_label.color = CASH_GREEN

    def toggle_connection(self, instance):
        self.is_connected = not self.is_connected
        if self.is_connected:
            self.connect_btn.text = "PROTECTED"
            self.connect_btn.background_color = CASH_GREEN
            self.ip_label.color = CASH_GREEN
            self.ip_label.text = f"IP: {self.current_server['ip']}"
            self.start_time = Clock.time()
            self.update_timer()
        else:
            self.connect_btn.text = "CONNECT"
            self.connect_btn.background_color = CASH_RED
            self.ip_label.color = TEXT_MUTED
            self.ip_label.text = "IP: 192.168.1.1"
            self.time_label.text = "Time: 00:00:00"

    def update_timer(self, dt=None):
        if not self.is_connected:
            return
        elapsed = int(Clock.time() - self.start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        self.time_label.text = f"Time: {h:02}:{m:02}:{s:02}"
        speed = random.randint(450, 750)
        self.speed_label.text = f"Speed: {speed} Kb/s"
        Clock.schedule_once(self.update_timer, 1)

if __name__ == '__main__':
    CashVPNApp().run()
