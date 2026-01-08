# Step-by-Step Pico Whale Deployment
# ====================================
# Follow these steps IN ORDER on your Pico W

print("🐋 Pico Whale - Let's Get You Running!")
print("=" * 50)
print("\nThis script will help verify your setup.")
print("Follow along and copy/paste these commands.\n")

# STEP 1: Verify MicroPython
print("\n📌 STEP 1: Verify MicroPython")
print("-" * 50)
print("Try running this command:")
print(">>> print('MicroPython OK!')")
print("\nIf you see 'MicroPython OK!' then continue.")
print("If you see an error, you need to flash MicroPython.\n")

# STEP 2: Check Files
print("\n📌 STEP 2: Check What Files Are On Your Pico")
print("-" * 50)
print("Copy and paste this:")
print("""
import os
print("Files on Pico:")
for f in os.listdir('/'):
    print(f"  - {f}")
""")
print("\nYou NEED: main.py, config.py")
print("You SHOULD HAVE: animations.py")
print()

# STEP 3: Check WiFi Config
print("\n📌 STEP 3: Verify WiFi Settings")
print("-" * 50)
print("Run this to check your config:")
print("""
try:
    from config import WIFI_SSID, WIFI_PASSWORD, DEVICE_ID
    print(f"WiFi SSID: {WIFI_SSID}")
    print(f"WiFi Password: {WIFI_PASSWORD}")
    print(f"Device ID: {DEVICE_ID}")
    print("✓ Config file found!")
except ImportError:
    print("✗ config.py not found - you need to upload it!")
""")
print()

# STEP 4: Test WiFi Connection
print("\n📌 STEP 4: Connect to WiFi")
print("-" * 50)
print("Run this (replace with YOUR WiFi if needed):")
print("""
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Use credentials from your config
from config import WIFI_SSID, WIFI_PASSWORD
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to WiFi...")
max_wait = 15
while max_wait > 0 and not wlan.isconnected():
    print(f"  Waiting... {max_wait}s")
    time.sleep(1)
    max_wait -= 1

if wlan.isconnected():
    print(f"✓ Connected! IP: {wlan.ifconfig()[0]}")
else:
    print("✗ Connection failed - check credentials!")
""")
print()

# STEP 5: Install umqtt
print("\n📌 STEP 5: Install MQTT Library (NEEDS WIFI!)")
print("-" * 50)
print("After WiFi is connected, run:")
print("""
import mip
print("Installing umqtt.simple...")
mip.install("umqtt.simple")
print("✓ Installation complete!")
""")
print()

# STEP 6: Verify umqtt
print("\n📌 STEP 6: Verify umqtt Library")
print("-" * 50)
print("Test if it's installed:")
print("""
try:
    from umqtt.simple import MQTTClient
    print("✓ umqtt.simple is installed and working!")
except ImportError:
    print("✗ umqtt not found - run Step 5 again")
""")
print()

# STEP 7: Run Main App
print("\n📌 STEP 7: Start the Main Application")
print("-" * 50)
print("If all above steps passed, reboot to run main.py:")
print("""
import machine
print("Rebooting Pico...")
machine.soft_reset()
""")
print("\nYou should see: '🐋 PICO WHALE STARTING UP! 🐋'")
print()

print("=" * 50)
print("💡 TIP: If you get stuck on any step, STOP and let me know!")
print("=" * 50)
