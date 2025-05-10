#!/bin/bash

# نصب virtualenv اگر نصب نیست
if ! python3 -m pip show virtualenv > /dev/null 2>&1; then
    echo "[+] Installing virtualenv..."
    python3 -m pip install --user virtualenv
fi

# ساخت محیط مجازی اگر وجود ندارد
if [ ! -d venv ]; then
    echo "[+] Creating virtual environment..."
    python3 -m virtualenv venv
fi

# فعال‌سازی محیط مجازی
source venv/bin/activate

# نصب پکیج‌ها
if [ -f requirements.txt ]; then
    echo "[+] Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
fi

echo "[✓] All dependencies installed in virtual environment." 