#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Social Auto App chalu thay chhe (PC + Mobile, ghar na WiFi par)..."
( sleep 2; (xdg-open http://localhost:8080 || open http://localhost:8080) >/dev/null 2>&1 ) &
python3 main.py --app --phone
