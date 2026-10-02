import tkinter as tk
from tkinter import messagebox
import platform
import socket
import getpass
import subprocess
import sys
import uuid
import os
import time


# =========================================================
# 507 // SYSTEM CONSOLE
# =========================================================

BG = "#050805"
PANEL = "#081008"
GREEN = "#00ff66"
DARK_GREEN = "#063d1b"
RED = "#ff2020"
WHITE = "#d8ffe5"
GRAY = "#6c8f77"


class App507:
    def __init__(self, root):
        self.root = root

        self.root.title("507 // SYSTEM CONSOLE")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.eye_x = 0
        self.eye_direction = 1
        self.blink = False
        self.wink = False
        self.red_eye = False

        self.build_ui()
        self.animate_eye()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        # Main background
        self.main = tk.Frame(
            self.root,
            bg=BG
        )
        self.main.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(
            self.main,
            bg=BG,
            height=150
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        # Canvas for logo + eye
        self.logo_canvas = tk.Canvas(
            header,
            bg=BG,
            highlightthickness=0
        )
        self.logo_canvas.pack(
            fill="both",
            expand=True
        )

        self.logo_canvas.bind(
            "<Configure>",
            lambda event: self.draw_header()
        )

        # Separator
        tk.Frame(
            self.main,
            bg=DARK_GREEN,
            height=2
        ).pack(fill="x")

        # Content
        content = tk.Frame(
            self.main,
            bg=BG
        )
        content.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=25
        )

        # Left panel
        left = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=DARK_GREEN,
            highlightthickness=1
        )
        left.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        tk.Label(
            left,
            text="SYSTEM MENU",
            bg=PANEL,
            fg=GREEN,
            font=("Consolas", 16, "bold")
        ).pack(
            pady=(25, 20),
            padx=30
        )

        self.make_button(
            left,
            "[ 1 ]  CMD ADMIN",
            self.cmd_admin
        )

        self.make_button(
            left,
            "[ 2 ]  DEVICE INFO",
            self.device_info
        )

        self.make_button(
            left,
            "[ 3 ]  DISCORD LOGIN",
            self.discord_login
        )

        self.make_button(
            left,
            "[ X ]  CLEAR",
            self.clear_output
        )

        # Right panel
        right = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=DARK_GREEN,
            highlightthickness=1
        )
        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            right,
            text="OUTPUT",
            bg=PANEL,
            fg=GREEN,
            font=("Consolas", 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        # Read-only output
        self.output = tk.Text(
            right,
            bg="#030603",
            fg=GREEN,
            insertbackground=GREEN,
            selectbackground=DARK_GREEN,
            relief="flat",
            borderwidth=0,
            font=("Consolas", 11),
            wrap="word",
            state="disabled"
        )
        self.output.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.write(
            "507 SYSTEM CONSOLE\n"
            "----------------------------\n"
            "STATUS : ONLINE\n"
            "MODE   : LOCAL\n"
            "SECURE : ENABLED\n\n"
            "Select an option from the menu.\n"
        )

        # Footer
        footer = tk.Label(
            self.main,
            text="507 // SHARP EYE // LOCAL SYSTEM TOOL",
            bg=BG,
            fg=GRAY,
            font=("Consolas", 9)
        )
        footer.pack(
            pady=(0, 10)
        )

    # =====================================================
    # BUTTON
    # =====================================================

    def make_button(self, parent, text, command):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg="#071307",
            fg=GREEN,
            activebackground=DARK_GREEN,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Consolas", 11, "bold"),
            width=24,
            height=2,
            cursor="hand2"
        )

        button.pack(
            padx=20,
            pady=7
        )

        return button

    # =====================================================
    # READ ONLY OUTPUT
    # =====================================================

    def write(self, text):

        self.output.config(state="normal")

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.insert(
            "end",
            text
        )

        self.output.config(
            state="disabled"
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_output(self):

        self.write(
            "507 SYSTEM CONSOLE\n"
            "----------------------------\n"
            "OUTPUT CLEARED.\n"
        )

        self.red_eye = False

    # =====================================================
    # CMD ADMIN
    # =====================================================

    def cmd_admin(self):

        try:

            subprocess.Popen(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Start-Process cmd -Verb RunAs"
                ]
            )

            self.write(
                "507 // CMD ADMIN\n"
                "----------------------------\n\n"
                "Administrator CMD launch requested.\n"
                "Windows UAC may ask for permission.\n"
            )

        except Exception as e:

            self.write(
                "507 // ERROR\n"
                "----------------------------\n\n"
                f"{e}"
            )

    # =====================================================
    # DEVICE INFO
    # =====================================================

    def device_info(self):

        self.red_eye = True

        hostname = socket.gethostname()

        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "Unavailable"

        username = getpass.getuser()

        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()

        machine = platform.machine()
        processor = platform.processor()
        python_version = platform.python_version()

        mac = ":".join(
            f"{(uuid.getnode() >> i) & 0xff:02x}"
            for i in range(
                40,
                -1,
                -8
            )
        )

        # Collect local IPs
        ips = []

        try:

            for info in socket.getaddrinfo(
                hostname,
                None
            ):

                ip = info[4][0]

                if ip not in ips:
                    ips.append(ip)

        except:
            pass

        if not ips:
            ips.append(local_ip)

        output = (
            "507 // DEVICE INFORMATION\n"
            "================================\n\n"

            f"USER           : {username}\n"
            f"HOSTNAME       : {hostname}\n\n"

            f"OS             : {os_name}\n"
            f"OS RELEASE     : {os_release}\n"
            f"OS VERSION     : {os_version}\n\n"

            f"MACHINE        : {machine}\n"
            f"PROCESSOR      : {processor or 'Unknown'}\n"
            f"PYTHON         : {python_version}\n\n"

            f"MAC ADDRESS    : {mac}\n\n"

            "IP ADDRESSES\n"
            "--------------------------------\n"
        )

        for ip in ips:
            output += f"• {ip}\n"

        output += (
            "\n================================\n"
            "LOCAL INFORMATION ONLY\n"
        )

        self.write(output)

    # =====================================================
    # DISCORD
    # =====================================================

    def discord_login(self):

        self.red_eye = False

        self.write(
            "507 // DISCORD LOGIN\n"
            "================================\n\n"

            "Discord authentication should use\n"
            "the official OAuth2 authorization flow.\n\n"

            "USER TOKENS ARE NOT ACCEPTED.\n\n"

            "No Discord token is stored or requested\n"
            "by this application.\n\n"

            "OAuth2 setup requires a Discord Developer\n"
            "Application and an authorized redirect URI.\n"
        )

    # =====================================================
    # HEADER DRAW
    # =====================================================

    def draw_header(self):

        canvas = self.logo_canvas

        canvas.delete("all")

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        center_y = height // 2

        # 507
        canvas.create_text(
            80,
            center_y,
            text="507",
            fill=GREEN,
            font=("Consolas", 55, "bold"),
            anchor="w"
        )

        canvas.create_text(
            85,
            center_y + 48,
            text="SHARP EYE",
            fill=GRAY,
            font=("Consolas", 10, "bold"),
            anchor="w"
        )

        # Eye position
        eye_center_x = width - 170 + self.eye_x
        eye_center_y = center_y

        # Outer eye
        eye_color = RED if self.red_eye else GREEN

        if self.blink:

            canvas.create_arc(
                eye_center_x - 90,
                eye_center_y - 25,
                eye_center_x + 90,
                eye_center_y + 25,
                start=200,
                extent=140,
                outline=eye_color,
                width=4
            )

            canvas.create_line(
                eye_center_x - 75,
                eye_center_y,
                eye_center_x + 75,
                eye_center_y,
                fill=eye_color,
                width=3
            )

        else:

            # Eye outline
            canvas.create_oval(
                eye_center_x - 90,
                eye_center_y - 38,
                eye_center_x + 90,
                eye_center_y + 38,
                outline=eye_color,
                width=4
            )

            # Inner eye
            canvas.create_oval(
                eye_center_x - 60,
                eye_center_y - 27,
                eye_center_x + 60,
                eye_center_y + 27,
                outline=DARK_GREEN if not self.red_eye else "#5a0000",
                width=2
            )

            # Pupil
            pupil_offset = self.eye_x // 3

            canvas.create_oval(
                eye_center_x - 15 + pupil_offset,
                eye_center_y - 15,
                eye_center_x + 15 + pupil_offset,
                eye_center_y + 15,
                fill=eye_color,
                outline=eye_color
            )

            # Pupil center
            canvas.create_oval(
                eye_center_x - 5 + pupil_offset,
                eye_center_y - 5,
                eye_center_x + 5 + pupil_offset,
                eye_center_y + 5,
                fill="#000000",
                outline="#000000"
            )

        # Little status light
        canvas.create_oval(
            width - 35,
            15,
            width - 20,
            30,
            fill=RED if self.red_eye else GREEN,
            outline=""
        )

    # =====================================================
    # ANIMATION
    # =====================================================

    def animate_eye(self):

        self.eye_x += self.eye_direction

        if self.eye_x >= 35:
            self.eye_direction = -1

        if self.eye_x <= -35:
            self.eye_direction = 1

        self.draw_header()

        # Random-looking timing without external packages
        now = int(time.time() * 10)

        if now % 47 == 0:
            self.blink = True
        else:
            self.blink = False

        self.root.after(
            70,
            self.animate_eye
        )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = App507(root)

    root.mainloop()
    