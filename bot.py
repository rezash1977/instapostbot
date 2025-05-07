import random
import os
import time
import schedule
import shutil
from dotenv import load_dotenv
from instagrapi import Client

# بارگذاری اطلاعات از .env
load_dotenv()
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# ورود
cl = Client()
cl.login(USERNAME, PASSWORD)

# مسیرها
MEDIA_FOLDER = "media"
POSTED_FOLDER = "posted_media"
POSTED_LOG = "posted_files.txt"

# لیست هشتگ‌ها
HASHTAGS = [
    "#photooftheday", "#love", "#nature", "#instagood", "#beautiful",
    "#style", "#travel", "#happy", "#life", "#python", "#AI", "#fun"
]

# ایجاد پوشه posted_media اگر وجود ندارد
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
    caption = f"پست خودکار با پایتون 🤖\n\n" + " ".join(random.sample(HASHTAGS, 5))

    try:
        if file.endswith(".mp4"):
            cl.video_upload(file_path, caption)
            print(f"✅ ویدیو پست شد: {file}")
        else:
            cl.photo_upload(file_path, caption)
            print(f"✅ عکس پست شد: {file}")

        save_posted_file(file)

        # انتقال فایل به posted_media
        shutil.move(file_path, os.path.join(POSTED_FOLDER, file))
        print(f"📁 فایل منتقل شد به پوشه {POSTED_FOLDER}")

    except Exception as e:
        print("❌ خطا هنگام آپلود:", e)

# زمان‌بندی
schedule.every().day.at("10:00").do(post_random_media)

print("⏳ ربات آماده است. منتظر زمان پست‌گذاری...")

while True:
    schedule.run_pending()
    time.sleep(60)
