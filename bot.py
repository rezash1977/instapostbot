import random
import os
import time
import shutil
from dotenv import load_dotenv
from instagrapi import Client

# بارگذاری اطلاعات از .env
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# ورود
cl = Client()
if os.path.exists("session.json"):
    cl.load_settings("session.json")
    cl.login(USERNAME, PASSWORD)
else:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")

# مسیرها
MEDIA_FOLDER = "media"
POSTED_FOLDER = "posted_media"
POSTED_LOG = "posted_files.txt"

# تابع خواندن هشتگ‌ها از فایل
HASHTAGS_FILE = "hashtags.txt"
def load_hashtags():
    if not os.path.exists(HASHTAGS_FILE):
        print(f"فایل {HASHTAGS_FILE} پیدا نشد!")
        return []
    with open(HASHTAGS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

os.makedirs(POSTED_FOLDER, exist_ok=True)

def get_posted_files():
    if not os.path.exists(POSTED_LOG):
        return []
    with open(POSTED_LOG, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def save_posted_file(filename):
    with open(POSTED_LOG, "a", encoding="utf-8") as f:
        f.write(filename + "\n")

def post_random_media():
    posted = get_posted_files()
    media_files = [
        f for f in os.listdir(MEDIA_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4")) and f not in posted
    ]

    if not media_files:
        print("🚫 فایل جدیدی برای پست نیست.")
        return

    file = random.choice(media_files)
    file_path = os.path.join(MEDIA_FOLDER, file)
    hashtags_list = load_hashtags()
    n = min(8, len(hashtags_list))
    if n > 0:
        selected_tags = random.sample(hashtags_list, n)
        hashtags = " ".join([f"#{tag}" for tag in selected_tags])
    else:
        hashtags = ""
    caption = f"پست خودکار با پایتون 🤖\n\n{hashtags}"

    try:
        if file.endswith(".mp4"):
            media = cl.video_upload(file_path, caption)
            print(f"✅ ویدیو پست شد: {file}")
        else:
            media = cl.photo_upload(file_path, caption)
            print(f"✅ عکس پست شد: {file}")

        # قرار دادن کامنت به صورت خودکار
        if n > 0:
            comment_text = " ".join([f"#{tag}" for tag in random.sample(hashtags_list, n)])
            time.sleep(5)  # تاخیر برای اطمینان از ثبت پست
            cl.media_comment(media.id, comment_text)
            print(f"💬 کامنت گذاشته شد: {comment_text}")

        save_posted_file(file)
        shutil.move(file_path, os.path.join(POSTED_FOLDER, file))
        print(f"📁 فایل منتقل شد به پوشه {POSTED_FOLDER}")

    except Exception as e:
        print("❌ خطا هنگام آپلود:", e)

def has_unposted_media():
    posted = get_posted_files()
    media_files = [
        f for f in os.listdir(MEDIA_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".mp4")) and f not in posted
    ]
    return len(media_files) > 0

if __name__ == "__main__":
    while has_unposted_media():
        post_random_media()
        if has_unposted_media():
            print("⏳ منتظر ۱۰ دقیقه بعدی...")
            time.sleep(600)
    print("✅ همه فایل‌های پوشه media پست شدند. برنامه پایان یافت.")
