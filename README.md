
# 📁 Telegram File Downloader

A powerful Python script that automatically joins Telegram channels, downloads document files, logs what’s downloaded, and sends real-time status updates to a Discord webhook.

---

## 🚀 Features

- ✅ Automatically joins specified Telegram channels.
- 📁 Downloads documents (e.g., `.zip`, `.txt`, `.pdf`) while skipping unwanted formats.(add your own extension to skip download)
- 🔄 Skips already-downloaded files to avoid duplicates.
- 📦 Logs all downloads and skipped files.
- 🌐 Sends status updates to a Discord webhook.
- 🛡️ Skips files larger than 2GB automatically.
- 📊 Uses progress bars for large downloads (via `tqdm`).

---

## ⚙️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/ranjan1560/Telegram-File-Downloader.git
cd telegram-file-downloader
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Configure the Script

Open the script and set your own values for:

```python
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK'
channels = ['channel_username_1', 'channel_username_2']
```

> 🔑 Get your `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org/).

---

## ▶️ How to Run

```bash
python3 telegram.py
```

The script will:

1. Join all channels in the list (if not already joined).
2. Check for document-type messages.
3. Download files under 2GB (except excluded extension).
4. Log all actions.
5. Send real-time status to your Discord channel via webhook.

---

## 📁 Logs & Downloads

All downloads and logs are saved in the `downloads/` directory:

```
downloads/
├── channel_username/
│   ├── downloaded_files.log
│   ├── not_downloaded.log
│   └── <your_files_here>
```

---

## 🧩 Customization

- **Skip File Types:** Change this list:
  ```python
  SKIP_EXTENSIONS = ['.mkv', '.mp4']
  ```

- **Auto Join Channels:** Disable auto-joining if already in them:
  ```python
  AUTO_JOIN_CHANNELS = False
  ```

---

## 🧪 Example Discord Notification

```
✅ Downloaded: sample.zip (14.2 MB)
```

Or on failure:
```
❌ Failed to download: logs.rar
Error: FloodWaitError: Wait for 30 seconds
```

---

## 🛑 Disclaimer

This script is for educational and automation purposes only. Respect privacy and Telegram's terms of service.

---

## 📬 Credits

Built by Ranjan Kumar.
