#!/bin/bash
# 🐋 Pico Whale - Deploy to Pico W from Command Line
# ==================================================
# This script uses mpremote to flash your Pico without VS Code!

set -e  # Exit on error

# Use full path to mpremote
MPREMOTE="/Users/jeffgoldner/Library/Python/3.9/bin/mpremote"

echo "🐋 Pico Whale Deployment Script"
echo "================================"
echo ""

# Check if mpremote is installed
if [ ! -f "$MPREMOTE" ]; then
    echo "⚠️  mpremote not found. Installing..."
    pip3 install mpremote
    MPREMOTE="/Users/jeffgoldner/Library/Python/3.9/bin/mpremote"
fi

# Check if Pico is connected
echo "📡 Checking for Pico W..."
if ! $MPREMOTE connect list &> /dev/null; then
    echo "❌ No Pico W found!"
    echo ""
    echo "Please:"
    echo "  1. Connect your Pico W via USB"
    echo "  2. Make sure MicroPython is installed"
    echo "  3. Run this script again"
    exit 1
fi

echo "✅ Pico W detected!"
echo ""

# Upload files
echo "📤 Uploading files to Pico..."
echo "  → Copying main.py..."
$MPREMOTE cp src/main.py :main.py

echo "  → Copying config.py..."
$MPREMOTE cp src/config.py :config.py

echo "  → Copying animations.py..."
$MPREMOTE cp src/animations.py :animations.py

echo "✅ All files uploaded!"
echo ""

# Verify files
echo "📋 Verifying files on Pico..."
$MPREMOTE exec "import os; print('Files:', os.listdir('/'))"
echo ""

# Check WiFi config
echo "🔧 Checking configuration..."
$MPREMOTE exec "from config import WIFI_SSID, DEVICE_ID; print(f'WiFi: {WIFI_SSID}'); print(f'Device: {DEVICE_ID}')"
echo ""

# Install umqtt if needed
echo "📦 Installing umqtt library (this requires WiFi on Pico)..."
$MPREMOTE exec "
import network
import time
from config import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print('Connecting to WiFi...')
max_wait = 20
while max_wait > 0 and not wlan.isconnected():
    time.sleep(1)
    max_wait -= 1

if wlan.isconnected():
    print('✅ WiFi connected!')
    print('Installing umqtt.simple...')
    import mip
    mip.install('umqtt.simple')
    print('✅ umqtt installed!')
else:
    print('❌ WiFi failed - check credentials in config.py')
"
echo ""

# Reboot to start main.py
echo "🔄 Rebooting Pico to start application..."
$MPREMOTE exec "import machine; machine.soft_reset()"

echo ""
echo "================================"
echo "✅ Deployment complete!"
echo "================================"
echo ""
echo "Your Pico Whale should now be running!"
echo "To view output, run: ./pico_repl.sh"
echo ""
