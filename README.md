# ⚡ Pandora Discord Control (ULTRA)

> A cyberpunk-inspired Discord management and monitoring tool with neon UI, matrix background, and real-time insights.

---

## 🚀 Overview

**Pandora Discord Control (ULTRA)** is a desktop application built with Python and PySide6 that provides:

* Real-time Discord server insights
* Webhook scanning
* Controlled server management tools
* A futuristic neon UI with matrix animation

This tool is designed for **administrators and developers** who want visibility and structured control over their Discord environments.

---

## ✨ Features

### 📡 Discord Monitoring

* Scan all servers the bot is in
* Extract and list all webhooks
* Save results to `webhooks.json`
* Live log output during scanning

---

### 📊 Live Stats Dashboard

* Total servers
* Total members
* Total channels
* Real-time system information:

  * Time
  * Local IP
  * Public IP
  * RAM usage
  * Disk usage

---

### ⚙️ Admin Tools (Safe Use)

* ✏️ Batch rename channels (prefix-based)
* 📢 Send a message to all channels (one-time broadcast)

> ⚠️ Requires appropriate Discord permissions

---

### 🎨 Cyberpunk UI

* Neon glow elements
* Electric-style buttons
* Matrix rain animated background
* Multi-panel layout
* Live progress bar

---

## 🧩 UI Layout

* **Left Panel**

  * Token input
  * Scan controls
  * Admin tools

* **Center Panel**

  * Live log output

* **Right Panel**

  * System info
  * Discord stats

---

## 🛠️ Requirements

* Python 3.11+ (recommended)
* pip

---

## 📦 Installation

```bash
git clone https://github.com/YOURNAME/pandora-discord-control.git
cd pandora-discord-control

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python discord_gui_ultra_safe.py
```

1. Enter your Discord Bot Token
2. Click **START SCAN**
3. Watch live output
4. Use admin tools if needed

---

## 📦 Build EXE

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build executable

```bash
pyinstaller --onefile --noconsole discord_gui_ultra_safe.py
```

### 3. Output

```plaintext
dist/
└── discord_gui_ultra_safe.exe
```

---

## 📁 Data Output

### webhooks.json

```json
[
  {
    "server": "Example Server",
    "webhooks": [
      {
        "channel": "general",
        "name": "WebhookName",
        "url": "https://discord.com/api/webhooks/..."
      }
    ]
  }
]
```

---

## 🔐 Permissions Required

Your bot must have:

* Manage Webhooks
* Manage Channels (for renaming)
* Send Messages (for broadcast)
* Read Messages / View Channels

---

## ⚠️ Disclaimer

This tool is intended for **legitimate administrative use only**.

* Only use on servers where you have permission
* Do not abuse automation features
* Follow Discord Terms of Service

---

## 🧠 Philosophy

Pandora is not just a tool.

It is a **control interface** —
where data becomes visible,
and systems become understandable.

---

## 📄 License

MIT License

---

## 🤝 Contributing

Contributions are welcome.
Please open an issue before major changes.

---

## 🌌 Final Thought

> "Control is not about destruction — it is about awareness."

Welcome to Pandora.