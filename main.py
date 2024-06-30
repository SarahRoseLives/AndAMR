from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineListItem
from kivy.clock import Clock
from socket import socket, AF_INET, SOCK_DGRAM
import threading
import re

KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "RTLAMR Output"

    MDScrollView:
        MDList:
            id: log_list
'''

class RTLAMRApp(MDApp):
    def build(self):
        self.main_widget = Builder.load_string(KV)
        self.scm_data = {}
        self.bind_socket()
        self.start_udp_listener()
        return self.main_widget

    def bind_socket(self):
        try:
            self.udp_sock = socket(AF_INET, SOCK_DGRAM)
            self.udp_sock.bind(('localhost', 8585))
            print("UDP socket bound successfully")
        except Exception as e:
            print(f"Error binding UDP socket: {e}")

    def start_udp_listener(self):
        # Start a new thread for UDP listening
        self.stop_event = threading.Event()
        self.listen_thread = threading.Thread(target=self.receive_udp)
        self.listen_thread.start()

    def receive_udp(self):
        try:
            while not self.stop_event.is_set():
                data, addr = self.udp_sock.recvfrom(1024)
                if data:
                    decoded_data = data.decode()
                    parsed_data = self.parse_udp_data(decoded_data)
                    if parsed_data:
                        # Use Clock.schedule_once to safely update the UI from the main thread
                        Clock.schedule_once(lambda dt: self.update_or_add_item(parsed_data))
        except Exception as e:
            print(f"Error receiving UDP: {e}")

    def parse_udp_data(self, data):
        """Parse UDP data into a dictionary of SCM data."""
        try:
            match = re.search(r"SCM:{ID:(\d+) Type:(\d+) Tamper:{Phy:(\d+) Enc:(\d+)} Consumption:\s+(\d+) CRC:(\w+)}", data)
            if match:
                scm_id = match.group(1)
                scm_type = match.group(2)
                phy_enc = match.group(3)
                consumption = match.group(5)

                return {
                    "id": scm_id,
                    "type": scm_type,
                    "phy_enc": phy_enc,
                    "consumption": consumption
                }
            else:
                print(f"Invalid UDP data format: {data}")
                return None

        except Exception as e:
            print(f"Error parsing UDP data: {e}")
            return None

    def update_or_add_item(self, data):
        scm_id = data.get("id")
        if not scm_id:
            print(f"Invalid data received: {data}")
            return

        scm_type = data.get("type", "")
        phy_enc = data.get("phy_enc", "")
        consumption = data.get("consumption", "")

        # Check if item already exists based on SCM ID
        if scm_id in self.scm_data:
            item = self.scm_data[scm_id]
            item.secondary_text = f"Type: {scm_type}, Consumption: {consumption}"
            item.tertiary_text = f"Tamper Phy: {phy_enc}"
        else:
            item = ThreeLineListItem(
                text=f"ID: {scm_id}, Type: {scm_type}",
                secondary_text=f"Consumption: {consumption}",
                tertiary_text=f"Tamper Phy: {phy_enc}"
            )
            self.scm_data[scm_id] = item
            self.main_widget.ids.log_list.add_widget(item)

    def on_stop(self):
        # Signal the UDP listener thread to stop
        self.stop_event.set()
        self.listen_thread.join()  # Wait for the thread to terminate
        self.udp_sock.close()  # Close the UDP socket

if __name__ == '__main__':
    RTLAMRApp().run()
