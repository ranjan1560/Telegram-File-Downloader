import os
import time
import requests
from tqdm import tqdm
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import MessageMediaDocument
from telethon.errors import FloodWaitError, ChannelPrivateError, ChatAdminRequiredError

# 🧾 CONFIGURATION

api_id = 1234567                    # ← Replace with your API ID
api_hash = '1a2b3c4d5e6f'           # ← Replace with your API Hash
channels = ['channel-1', 'channel-2']
base_download_dir = 'downloads'
AUTO_JOIN_CHANNELS = True
SKIP_EXTENSIONS = ['.mkv', '.mp4']  # ← Extensions to skip
WEBHOOK_URL = 'Your_WEBHook_URL'    # ← Replace with your Webhook URL

os.makedirs(base_download_dir, exist_ok=True)

client = TelegramClient('file_downloader', api_id, api_hash)

# 📏 Utility: Convert bytes to MB
def human_readable_size(size_bytes):
    return f"{round(size_bytes / (1024 * 1024), 2)} MB"

# ❌ Should skip by extension?
def should_skip_file(filename):
    return any(filename.lower().endswith(ext) for ext in SKIP_EXTENSIONS)

# 🌐 Send webhook message
def send_webhook_notification(message):
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"content": message})  # ✅ FIXED KEY HERE
        except Exception as e:
            print(f"⚠️ Failed to send webhook: {e}")

# 🚀 Start session
with client:
    for channel in channels:
        print(f"\n📥 Channel: {channel}")

        if AUTO_JOIN_CHANNELS:
            try:
                client(JoinChannelRequest(channel))
                print(f"✅ Joined {channel}")
            except (ChannelPrivateError, ChatAdminRequiredError):
                print(f"❌ Can't join {channel} — private or admin-only.")
                continue
            except Exception as e:
                print(f"⚠️ Join issue: {e}")

        download_dir = os.path.join(base_download_dir, channel)
        os.makedirs(download_dir, exist_ok=True)
        log_file_path = os.path.join(download_dir, 'downloaded_files.log')
        not_downloaded_log_path = os.path.join(download_dir, 'not_downloaded.log')

        downloaded_files = set()
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                downloaded_files = set(line.strip() for line in log_file)

        print("🔄 Fetching messages...")
        try:
            all_messages = list(client.iter_messages(channel))
        except Exception as e:
            print(f"❌ Error fetching messages: {e}")
            continue

        media_messages = [msg for msg in all_messages if msg.media and isinstance(msg.media, MessageMediaDocument)]
        total_files = len(media_messages)
        print(f"📦 Total files to download: {total_files}")

        downloaded_count = 0
        skipped_count = 0

        for msg in tqdm(media_messages, desc=f"Downloading from {channel}", unit='file'):
            try:
                filename = msg.file.name or f"{msg.id}"
                filepath = os.path.join(download_dir, filename)

                if filename in downloaded_files or os.path.exists(filepath):
                    skipped_count += 1
                    continue

                if should_skip_file(filename):
                    print(f"⏭️ Skipping {filename} (filtered by extension)")
                    skipped_count += 1
                    continue

                total_size = msg.file.size or 0

                if total_size > 2 * 1024 * 1024 * 1024:
                    reason = f"{filename} — Not downloaded (Above 2GB: {human_readable_size(total_size)})"
                    with open(not_downloaded_log_path, 'a') as nd_log:
                        nd_log.write(reason + '\n')
                    send_webhook_notification(f"⚠️ Skipped (2GB+): {filename}")
                    continue

                progress_bar = tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"⬇️ {filename}",
                    leave=False
                )

                def progress_callback(current, total):
                    progress_bar.n = current
                    progress_bar.refresh()

                print(f"\n📁 Downloading: {filename} ({human_readable_size(total_size)})")
                client.download_media(message=msg, file=filepath, progress_callback=progress_callback)
                progress_bar.close()

                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"{filename}\n")

                send_webhook_notification(f"✅ Downloaded: {filename} ({human_readable_size(total_size)})")
                downloaded_count += 1
                time.sleep(0.2)

            except FloodWaitError as e:
                print(f"⏳ Flood wait: sleeping {e.seconds} sec")
                time.sleep(e.seconds)
            except Exception as e:
                error_reason = f"{filename} — Failed: {str(e)}"
                with open(not_downloaded_log_path, 'a') as nd_log:
                    nd_log.write(error_reason + '\n')
                send_webhook_notification(f"❌ Failed to download: {filename}\nError: {e}")
                continue

        print(f"\n✅ Done with {channel}")
        print(f"🔽 Downloaded: {downloaded_count}")
        print(f"⏭️ Skipped: {skipped_count}")
        send_webhook_notification(f"📦 Completed channel: {channel}\n✅ {downloaded_count} downloaded, ⏭️ {skipped_count} skipped.")
