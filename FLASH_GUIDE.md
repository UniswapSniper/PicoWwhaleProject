# 🐋 Pico Whale Project - Flash Guide

> **Quick Reference:** Step-by-step guide to properly flash your Pico Whale firmware

## 📋 Required Files

Your Pico W needs these files in the **root directory**:

```
/ (root)
├── main.py           # Main application (auto-runs)
├── config.py         # WiFi & device settings
└── animations.py     # LED patterns (optional)
```

## 🚀 Quick Start

### 1. Install MicroPython

Download from: https://micropython.org/download/rp2-pico-w/

1. Hold **BOOTSEL** button on Pico W
2. Plug in USB while holding
3. Drag `.uf2` file to `RPI-RP2` drive
4. Pico reboots automatically

### 2. Install umqtt Library

Connect to REPL in VS Code (`Cmd+Shift+P` → "Pico-W-Go: Connect"), then:

```python
import network, mip

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YOUR_WIFI", "YOUR_PASSWORD")

# Install library
mip.install("umqtt.simple")
```

### 3. Configure Settings

Edit `src/config.py`:

```python
WIFI_SSID = "YourWiFi"
WIFI_PASSWORD = "YourPassword"
DEVICE_ID = "whale_1"  # or "whale_2" for second whale
```

### 4. Upload Files

**Using Pico-W-Go:**

1. Right-click each file in `src/` folder
2. Select "Upload current file to Pico"
3. Upload: `main.py`, `config.py`, `animations.py`

**Verify upload:**
```python
import os
print(os.listdir('/'))  # Should show your files
```

### 5. Test & Run

**Run diagnostic:**
```python
import quick_test  # Tests all hardware
```

**Start main app:**
```python
import machine
machine.soft_reset()
```

Should see:
```
🐋 PICO WHALE STARTING UP! 🐋
✓ Connected! IP: x.x.x.x
✓ MQTT connected!
✓ READY!
```

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: umqtt" | Run step 2 again |
| "WiFi failed" | Check credentials, use 2.4GHz network |
| "MQTT failed" | Check internet connection, firewall |
| Touch not working | Verify GPIO15 wiring, check `config.py` |

## 📞 Full Documentation

See [setup_guide.md](docs/setup_guide.md) for detailed instructions and troubleshooting.

---

**Current Config:** WiFi: FX3100-E8EA • Device: whale_1 • Using onboard LED
