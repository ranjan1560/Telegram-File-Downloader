
# 📁 Telegram File Downloader

This script uses the **Telethon** library to automatically download all files from specified public Telegram channels. It supports:

- ✅ Multi-channel support
- 🧠 Resume support (via .log file)
- 📦 Per-channel file storage
- 📊 Live download progress with size and percent
- 🛠 Auto-join public channels
- 🧱 Handles large files (up to 2GB)

---

## 🚀 How to Use

### 1. Install Dependencies

```bash
pip install telethon tqdm
```

---

### 2. Get Telegram API Credentials

- Go to: https://my.telegram.org
- Log in and click **API Development Tools**
- Create an app and get:
  - **API ID**
  - **API Hash**

---

### 3. Configure the Script

Update the script with your API ID and Hash:

```python
api_id = 123456
api_hash = 'your_api_hash'
channels = ['YourChannelUsername']  # Add channel usernames (no @)
```

---

### 4. Run the Script

```bash
python3 telegram_file_downloader.py
```

---

## 📂 Output Structure

```
downloads/
├── ChannelName/
│   ├── file1.zip
│   ├── file2.rar
│   └── downloaded_files.log
```

---

## 📈 Features Explained

- **Automatic joining** of public channels
- **Only downloads documents/media**
- **Skips previously downloaded files**
- **Tracks progress in MB and % using tqdm**
- **Catches Telegram rate limits (FloodWaitError)**

---

## 🚫 Limitations

### Telegram API has a 2GB file size limit.

| Upload Type | Max File Size |
|-------------|----------------|
| User API (Telethon) | 2 GB |
| Bot API | 2 GB |
| Telegram Premium | 4 GB (not accessible via API) |

Files larger than 2GB will not download and will raise an error.

---
