from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import MessageMediaDocument
from telethon.errors import FloodWaitError, ChannelPrivateError, ChatAdminRequiredError
import os
import time
from tqdm import tqdm

# 🔑 Replace with your Telegram API credentials
api_id = 123456
api_hash = 'your_api_hash'

channels = ['channel_one', 'channel_two']
base_download_dir = 'downloads'
os.makedirs(base_download_dir, exist_ok=True)

AUTO_JOIN_CHANNELS = True

client = TelegramClient('file_downloader', api_id, api_hash)

def human_readable_size(size_bytes):
    return f"{round(size_bytes / (1024 * 1024), 2)} MB"

with client:
    for channel in channels:
        print(f"\n📥 Channel: {channel}")

        if AUTO_JOIN_CHANNELS:
            try:
                client(JoinChannelRequest(channel))
                print(f"✅ Joined {channel}")
            except (ChannelPrivateError, ChatAdminRequiredError):
                print(f"❌ Can't join {channel} — might be private or need admin.")
                continue
            except Exception as e:
                print(f"⚠️ Already joined or other issue: {e}")

        download_dir = os.path.join(base_download_dir, channel)
        os.makedirs(download_dir, exist_ok=True)

        log_file_path = os.path.join(download_dir, 'downloaded_files.log')
        downloaded_files = set()
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                downloaded_files = set(line.strip() for line in log_file)

        print("🔄 Fetching messages...")
        try:
            all_messages = list(client.iter_messages(channel))
        except Exception as e:
            print(f"❌ Error fetching messages from {channel}: {e}")
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

                total_size = msg.file.size or 0
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

                downloaded_count += 1
                time.sleep(0.2)

            except FloodWaitError as e:
                print(f"⏳ Flood wait. Sleeping {e.seconds} seconds.")
                time.sleep(e.seconds)
            except Exception as e:
                print(f"❌ Error downloading message {msg.id}: {e}")
                continue

        print(f"\n✅ Finished {channel}")
        print(f"🔽 Downloaded: {downloaded_count}")
        print(f"⏭️ Skipped: {skipped_count}")
