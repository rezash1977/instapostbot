    #!/bin/bash

    # گرفتن یوزرنیم و پسورد اینستاگرام
    read -p "Instagram Username: " IG_USERNAME
    read -s -p "Instagram Password: " IG_PASSWORD

    echo -e "\nIG_USERNAME=$IG_USERNAME\nIG_PASSWORD=$IG_PASSWORD" > .env

    echo "[+] .env file created."

    # ساخت فایل hashtags.txt اگر وجود ندارد
    if [ ! -f hashtags.txt ]; then
        echo -e "photooftheday\nlove\nnature\nنوروز\nبهار\nخلاقیت" > hashtags.txt
        echo "[+] hashtags.txt created."
    fi

    # ساخت فایل posted_files.txt اگر وجود ندارد
    if [ ! -f posted_files.txt ]; then
        touch posted_files.txt
        echo "[+] posted_files.txt created."
    fi

    # ساخت پوشه media و posted_media اگر وجود ندارند
    if [ ! -d media ]; then
        mkdir media
        echo "[+] media directory created."
    fi
    if [ ! -d posted_media ]; then
        mkdir posted_media
        echo "[+] posted_media directory created."
    fi

    # ساخت requirements.txt اگر وجود ندارد
    if [ ! -f requirements.txt ]; then
        echo -e "instagrapi\npython-dotenv\nshutil" > requirements.txt
        echo "[+] requirements.txt created."
    fi

    echo "[✓] Setup complete. Now installing Python packages..."
    pip install -r requirements.txt 