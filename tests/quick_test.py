# Quick Diagnostic Test for Pico Whale
# =====================================
# Upload this file to your Pico to test all hardware components
# Run with: import quick_test

import time
from machine import Pin

print("\n" + "=" * 50)
print("🐋 PICO WHALE HARDWARE DIAGNOSTIC")
print("=" * 50 + "\n")

# Test 1: Onboard LED
print("Test 1: Onboard LED")
print("-" * 30)
try:
    led = Pin("LED", Pin.OUT)
    print("  Blinking LED 3 times...")
    for i in range(3):
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)
    print("  ✓ Onboard LED working!")
except Exception as e:
    print(f"  ✗ LED Error: {e}")

# Test 2: Touch Sensor
print("\nTest 2: Touch Sensor (GPIO15)")
print("-" * 30)
try:
    touch = Pin(15, Pin.IN, Pin.PULL_DOWN)
    print("  Touch the sensor within 5 seconds...")
    touched = False
    for i in range(50):
        if touch.value() == 1:
            print("  ✓ Touch detected! Sensor working!")
            touched = True
            break
        time.sleep(0.1)
    if not touched:
        print("  ⚠ No touch detected - check wiring or try again")
except Exception as e:
    print(f"  ✗ Touch Sensor Error: {e}")

# Test 3: WiFi
print("\nTest 3: WiFi Connection")
print("-" * 30)
try:
    import network
    from config import WIFI_SSID, WIFI_PASSWORD
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        print(f"  ✓ Already connected! IP: {wlan.ifconfig()[0]}")
    else:
        print(f"  Connecting to: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        max_wait = 15
        while max_wait > 0 and not wlan.isconnected():
            print(f"    Waiting... {max_wait}s")
            time.sleep(1)
            max_wait -= 1
        
        if wlan.isconnected():
            print(f"  ✓ WiFi connected! IP: {wlan.ifconfig()[0]}")
        else:
            print("  ✗ WiFi connection failed!")
            print("    Check SSID and password in config.py")
except Exception as e:
    print(f"  ✗ WiFi Error: {e}")

# Test 4: MQTT Library
print("\nTest 4: MQTT Library")
print("-" * 30)
try:
    from umqtt.simple import MQTTClient
    print("  ✓ umqtt.simple imported successfully!")
except ImportError:
    print("  ✗ umqtt.simple NOT FOUND!")
    print("    Install with: mip.install('umqtt.simple')")
except Exception as e:
    print(f"  ✗ MQTT Library Error: {e}")

# Test 5: Config File
print("\nTest 5: Configuration")
print("-" * 30)
try:
    from config import (
        DEVICE_ID, WHALE_PAIR_ID, 
        USE_NEOPIXEL, USE_SERVO, USE_SOUND_SENSOR
    )
    print(f"  Device ID: {DEVICE_ID}")
    print(f"  Pair ID: {WHALE_PAIR_ID}")
    print(f"  NeoPixel: {'Enabled' if USE_NEOPIXEL else 'Disabled'}")
    print(f"  Servo: {'Enabled' if USE_SERVO else 'Disabled'}")
    print(f"  Sound Sensor: {'Enabled' if USE_SOUND_SENSOR else 'Disabled'}")
    print("  ✓ Config loaded successfully!")
except Exception as e:
    print(f"  ✗ Config Error: {e}")

# Test 6: File System
print("\nTest 6: File System Check")
print("-" * 30)
try:
    import os
    files = os.listdir('/')
    print("  Files on Pico:")
    for f in files:
        print(f"    - {f}")
    
    required = ['main.py', 'config.py']
    recommended = ['animations.py']
    
    missing = []
    for f in required:
        if f not in files:
            missing.append(f)
    
    if missing:
        print(f"  ✗ Missing required files: {', '.join(missing)}")
    else:
        print("  ✓ All required files present!")
    
    if 'animations.py' in files:
        print("  ✓ animations.py found (recommended)")
    else:
        print("  ⚠ animations.py not found (optional)")
        
except Exception as e:
    print(f"  ✗ File System Error: {e}")

# Summary
print("\n" + "=" * 50)
print("🐋 DIAGNOSTIC COMPLETE")
print("=" * 50)
print("\nNext Steps:")
print("1. Fix any errors shown above")
print("2. Run: import machine; machine.soft_reset()")
print("3. Main application should auto-start")
print("\n")
