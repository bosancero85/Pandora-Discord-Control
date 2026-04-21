import sys
import json
import asyncio
import discord
import random
import psutil
import requests
import socket
from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# =========================
# MATRIX BACKGROUND
# =========================

class MatrixRain(QWidget):
    def __init__(self):
        super().__init__()
        self.chars = [chr(i) for i in range(33, 126)]
        self.columns = [0] * 120

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 40))

        for i in range(len(self.columns)):
            if random.random() < 0.1:
                continue

            char = random.choice(self.chars)
            x = i * 10
            y = self.columns[i]

            painter.setPen(QColor(0, 255, 255))
            painter.drawText(x, y, char)

            self.columns[i] += 10
            if self.columns[i] > self.height():
                self.columns[i] = 0


# =========================
# GLOW EFFECT
# =========================

def glow(widget):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(25)
    effect.setColor(QColor("#00ffff"))
    effect.setOffset(0)
    widget.setGraphicsEffect(effect)


# =========================
# SYSTEM INFO
# =========================

def get_info():
    try:
        public_ip = requests.get("https://api.ipify.org").text
    except:
        public_ip = "N/A"

    return f"""
🕒 {datetime.now().strftime("%H:%M:%S")}
🌐 Public IP: {public_ip}
💻 Local IP: {socket.gethostbyname(socket.gethostname())}
🧠 RAM: {psutil.virtual_memory().percent}%
💾 Disk: {psutil.disk_usage('/').percent}%
"""


# =========================
# SCAN THREAD
# =========================

class ScanThread(QThread):
    log = Signal(str)
    progress = Signal(int)
    stats = Signal(dict)

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.client = None

    def run(self):
        asyncio.run(self.scan())

    async def scan(self):
        self.client = discord.Client(intents=discord.Intents.default())
        results = []

        @self.client.event
        async def on_ready():
            self.log.emit(f"⚡ Connected as {self.client.user}")

            stats = {
                "servers": len(self.client.guilds),
                "members": sum(g.member_count for g in self.client.guilds),
                "channels": sum(len(g.channels) for g in self.client.guilds)
            }
            self.stats.emit(stats)

            total = len(self.client.guilds)
            count = 0

            for guild in self.client.guilds:
                count += 1
                self.progress.emit(int((count / total) * 100))

                self.log.emit(f"\n🌐 {guild.name}")

                guild_data = {"server": guild.name, "webhooks": []}

                for ch in guild.text_channels:
                    try:
                        hooks = await ch.webhooks()
                        for h in hooks:
                            self.log.emit(f"  ⚡ {h.name} | #{ch.name}")
                            guild_data["webhooks"].append({
                                "channel": ch.name,
                                "name": h.name,
                                "url": h.url
                            })
                    except:
                        continue

                results.append(guild_data)

            with open("webhooks.json", "w") as f:
                json.dump(results, f, indent=4)

            self.log.emit("\n✅ Scan complete")
            self.progress.emit(100)

        await self.client.start(self.token)


# =========================
# MAIN WINDOW
# =========================

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("⚡ Pandora Discord Control")
        self.resize(950, 700)

        self.matrix = MatrixRain()
        self.matrix.setParent(self)
        self.matrix.lower()

        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: rgba(10,10,10,180);")

        main = QHBoxLayout(self.container)

        # LEFT PANEL
        left = QVBoxLayout()

        self.token = QLineEdit()
        self.token.setPlaceholderText("Bot Token")
        glow(self.token)

        self.start = QPushButton("START SCAN")
        glow(self.start)
        self.start.clicked.connect(self.run_scan)

        self.renameInput = QLineEdit()
        self.renameInput.setPlaceholderText("Rename Prefix")

        self.renameBtn = QPushButton("Rename Channels")
        glow(self.renameBtn)
        self.renameBtn.clicked.connect(self.rename_channels)

        self.msgInput = QLineEdit()
        self.msgInput.setPlaceholderText("Broadcast Message")

        self.broadcastBtn = QPushButton("Send Message Once")
        glow(self.broadcastBtn)
        self.broadcastBtn.clicked.connect(self.broadcast_once)

        self.progress = QProgressBar()
        glow(self.progress)

        left.addWidget(self.token)
        left.addWidget(self.start)
        left.addWidget(self.renameInput)
        left.addWidget(self.renameBtn)
        left.addWidget(self.msgInput)
        left.addWidget(self.broadcastBtn)
        left.addWidget(self.progress)

        # CENTER LOG
        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        self.logbox.setStyleSheet("color:#00ffff;background:#000;")
        glow(self.logbox)

        # RIGHT PANEL
        right = QVBoxLayout()

        self.statsLabel = QLabel("Stats...")
        glow(self.statsLabel)

        self.sysinfo = QLabel()
        glow(self.sysinfo)

        self.exit = QPushButton("EXIT")
        self.exit.clicked.connect(self.close)
        glow(self.exit)

        right.addWidget(self.statsLabel)
        right.addWidget(self.sysinfo)
        right.addWidget(self.exit)

        main.addLayout(left, 1)
        main.addWidget(self.logbox, 3)
        main.addLayout(right, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(2000)

    def resizeEvent(self, e):
        self.matrix.resize(self.size())
        self.container.resize(self.size())

    def update_info(self):
        self.sysinfo.setText(get_info())

    def run_scan(self):
        token = self.token.text().strip()
        if not token:
            self.logbox.append("❌ Missing token")
            return

        self.thread = ScanThread(token)
        self.thread.log.connect(self.logbox.append)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.stats.connect(self.update_stats)
        self.thread.start()

    def update_stats(self, stats):
        self.statsLabel.setText(
            f"Servers: {stats['servers']}\n"
            f"Members: {stats['members']}\n"
            f"Channels: {stats['channels']}"
        )

    def rename_channels(self):
        prefix = self.renameInput.text().strip()
        if not prefix:
            self.logbox.append("❌ Enter prefix")
            return

        async def task():
            for g in self.thread.client.guilds:
                for ch in g.text_channels:
                    try:
                        await ch.edit(name=f"{prefix}-{ch.name}")
                    except:
                        continue

        asyncio.run(task())
        self.logbox.append("✅ Channels renamed")

    def broadcast_once(self):
        msg = self.msgInput.text().strip()
        if not msg:
            self.logbox.append("❌ Enter message")
            return

        async def task():
            for g in self.thread.client.guilds:
                for ch in g.text_channels:
                    try:
                        await ch.send(msg)
                    except:
                        continue

        asyncio.run(task())
        self.logbox.append("✅ Message sent")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())