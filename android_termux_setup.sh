#!/data/data/com.termux/files/usr/bin/bash
# 📱 Juna Android phone par 24 kalak chalavo (Termux).
# 1) F-Droid mathi "Termux" install karo (Play Store vali juni chhe)
# 2) App folder phone ma copy karo, Termux ma te folder ma jai: bash android_termux_setup.sh
set -e
pkg update -y
pkg install -y python ffmpeg libjpeg-turbo libpng freetype termux-api
pip install --upgrade pip
pip install requests Pillow edge-tts
termux-wake-lock || true       # phone sui jay topan app chalu rahe
echo ""
echo "✅ Taiyar! Have chalavo:  python main.py --app --phone"
echo "   Phone ne charger par rakho, ane Settings → Battery ma Termux ne 'Unrestricted' karo."
