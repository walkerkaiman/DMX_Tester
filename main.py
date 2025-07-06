import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time
import socket
import struct

class DMXTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DMX Tester")
        self.serial_port = None
        self.running = False
        self.dmx_buffer = bytearray(513)
        self.dmx_buffer[0] = 0x00
        self.last_log_time = 0
        self.baudrate = 250000
        self.protocol = "Serial"
        self.artnet_ip = "127.0.0.1"
        self.universe = 0
        self.sacn_sequence = 0

        self.setup_gui()

    def setup_gui(self):
        self.root.geometry("700x900")
        self.root.resizable(False, True)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        port_frame = ttk.LabelFrame(main_frame, text="DMX Output")
        port_frame.pack(fill="x", padx=5, pady=5)

        self.protocol_var = tk.StringVar()
        self.protocol_dropdown = ttk.Combobox(port_frame, textvariable=self.protocol_var, width=10, values=["Serial", "Art-Net", "sACN"])
        self.protocol_dropdown.current(0)
        self.protocol_dropdown.pack(side="left", padx=5)
        self.protocol_dropdown.bind("<<ComboboxSelected>>", self.update_output_fields)

        self.port_var = tk.StringVar()
        self.port_dropdown = ttk.Combobox(port_frame, textvariable=self.port_var, width=30)
        self.port_dropdown.pack(side="left", padx=5)
        self.refresh_ports()

        self.artnet_ip_label = ttk.Label(port_frame, text="Node IP:")
        self.artnet_ip_entry = ttk.Entry(port_frame, width=15)
        self.artnet_ip_entry.insert(0, "127.0.0.1")

        self.universe_label = ttk.Label(port_frame, text="Universe:")
        self.universe_var = tk.IntVar(value=0)
        self.universe_dropdown = ttk.Combobox(port_frame, textvariable=self.universe_var, width=5, values=list(range(256)))
        self.universe_dropdown.current(0)

        self.connect_button = ttk.Button(port_frame, text="Connect", command=self.connect_output)
        self.connect_button.pack(side="left", padx=5)

        self.update_output_fields()

        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_frame_id, width=e.width))

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.sliders = []
        for i in range(1, 513):
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill="x", padx=5, pady=1)

            label = ttk.Label(frame, text=f"Ch {i}", width=6)
            label.pack(side="left")

            slider = ttk.Scale(frame, from_=0, to=255, orient="horizontal")
            slider.pack(side="left", fill="x", expand=True, padx=5)

            value_label = ttk.Label(frame, text="0", width=4)
            value_label.pack(side="left", padx=5)

            def update_label(event=None, s=slider, ch=i, lbl=value_label):
                val = int(float(s.get()))
                lbl.config(text=str(val))
                self.dmx_buffer[ch] = val

            slider.bind("<Motion>", update_label)
            slider.bind("<ButtonRelease-1>", update_label)
            self.sliders.append(slider)

        log_frame = ttk.LabelFrame(main_frame, text="DMX Stream Log")
        log_frame.pack(fill="both", expand=False, padx=5, pady=5)

        self.log_box = scrolledtext.ScrolledText(log_frame, height=10, width=90, state="disabled")
        self.log_box.pack(fill="both", expand=True, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_dropdown['values'] = [port.device for port in ports]
        if ports:
            self.port_dropdown.current(0)

    def update_output_fields(self, event=None):
        selection = self.protocol_var.get()

        if selection == "Serial":
            self.port_dropdown.pack(side="left", padx=5)
            self.artnet_ip_label.pack_forget()
            self.artnet_ip_entry.pack_forget()
            self.universe_label.pack_forget()
            self.universe_dropdown.pack_forget()
        elif selection == "Art-Net":
            self.port_dropdown.pack_forget()
            self.artnet_ip_label.pack(side="left", padx=5)
            self.artnet_ip_entry.pack(side="left", padx=5)
            self.universe_label.pack(side="left", padx=5)
            self.universe_dropdown.pack(side="left", padx=5)
        elif selection == "sACN":
            self.port_dropdown.pack_forget()
            self.artnet_ip_label.pack_forget()
            self.artnet_ip_entry.pack_forget()
            self.universe_label.pack(side="left", padx=5)
            self.universe_dropdown.pack(side="left", padx=5)

    def connect_output(self):
        self.running = True
        self.protocol = self.protocol_var.get()
        self.universe = self.universe_var.get()

        if self.protocol == "Serial":
            try:
                self.serial_port = serial.Serial(self.port_var.get(), self.baudrate)
                self.log(f"[CONNECTED] Serial on {self.port_var.get()}")
            except Exception as e:
                self.log(f"[ERROR] Serial connect: {e}")
                return
        elif self.protocol == "Art-Net":
            self.artnet_ip = self.artnet_ip_entry.get()
            self.log(f"[CONNECTED] Art-Net to {self.artnet_ip}, Universe {self.universe}")
        elif self.protocol == "sACN":
            self.log(f"[CONNECTED] sACN Universe {self.universe}")

        self.start_sender_thread()

    def start_sender_thread(self):
        def send_loop():
            while self.running:
                try:
                    if self.protocol == "Serial" and self.serial_port and self.serial_port.is_open:
                        self.serial_port.break_condition = True
                        time.sleep(0.001)
                        self.serial_port.break_condition = False
                        self.serial_port.write(self.dmx_buffer)
                    elif self.protocol == "Art-Net":
                        self.send_artnet()
                    elif self.protocol == "sACN":
                        self.send_sacn()

                    if time.time() - self.last_log_time > 1.0:
                        preview = "  ".join([f"{i}:{self.dmx_buffer[i]:>3}" for i in range(1, 17)])
                        self.log(f"[DMX] {preview}")
                        self.last_log_time = time.time()

                    time.sleep(1 / 30.0)
                except Exception as e:
                    self.log(f"[ERROR] Send loop: {e}")
                    break

        threading.Thread(target=send_loop, daemon=True).start()

    def send_artnet(self):
        header = bytearray(b'Art-Net\x00') + bytearray([0x00, 0x50]) + bytearray([0x00, 14])
        header += bytearray([0x00, 0x00])  # sequence + physical
        header += struct.pack('<H', self.universe)  # little-endian universe
        header += struct.pack('>H', 512)  # big-endian length
        packet = header + self.dmx_buffer[1:]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (self.artnet_ip, 6454))
        sock.close()

    def send_sacn(self):
        multicast_ip = f"239.255.0.{self.universe & 0xFF}"
        port = 5568
        cid = b'\x01' * 16
        source_name = b'DMX Tester'
        priority = 100
        sequence = self.sacn_sequence % 256
        self.sacn_sequence += 1

        root_layer = struct.pack('>HH16s', 0x0010, 0x7000 | 0x002E, cid)
        framing_layer = struct.pack('>HH64sBBH', 0x0002, 0x7000 | 0x0028, source_name.ljust(64, b'\x00'), priority, sequence, 0)
        dmp_layer = b'\x02\xA1\x00\x00\x00\x01\x02' + struct.pack('>H', 513) + self.dmx_buffer

        pdu = root_layer + framing_layer + dmp_layer
        header = b'\x00\x10' + struct.pack('>H', 0x7000 | len(pdu)) + b'ASC-E1.17\x00\x00\x00'
        packet = header + pdu

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
        sock.sendto(packet, (multicast_ip, port))
        sock.close()

    def log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.yview(tk.END)
        self.log_box.configure(state="disabled")

    def on_close(self):
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            for i in range(1, 513):
                self.dmx_buffer[i] = 0
            self.serial_port.write(self.dmx_buffer)
            self.serial_port.close()
        self.root.destroy()

root = tk.Tk()
app = DMXTesterApp(root)
root.mainloop()
