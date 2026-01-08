# 🐋 Pico Whale Project

A connected whale pair system using Raspberry Pi Pico W microcontrollers. When you touch one whale, the other responds with beautiful LED animations - creating a tangible connection across any distance!

![Status](https://img.shields.io/badge/status-ready--for--deployment-brightgreen)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%20Pico%20W-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- **Touch-Activated Communication** - Touch your whale to send a signal to your friend's whale
- **Beautiful LED Animations** - 14 different patterns including pulse, rainbow, wave, sparkle, and more
- **Real-Time MQTT Networking** - Instant communication between locations worldwide
- **Web Control Panel** - Beautiful browser-based interface to control your whales
- **Desktop Simulator** - Test the entire system without any hardware
- **Offline Demo Mode** - Works without internet for testing
- **Heartbeat System** - Know when your whale is online

---

## 🚀 Quick Start

### Option 1: Test Without Hardware (Recommended First!)

```bash
# 1. Install dependency
pip install paho-mqtt

# 2. Run the desktop simulator
cd "Pico Whale Project/tools"
python desktop_simulator.py
```

### Option 2: Run the Web Control Panel

```bash
# Simply open in your browser
cd "Pico Whale Project/web"
open index.html   # macOS
# OR just double-click index.html
```

### Option 3: Deploy to Real Hardware

See [Full Setup Guide](docs/setup_guide.md) for detailed instructions.

---

## 📁 Project Structure

```
Pico Whale Project/
├── 📱 src/                      # Pico W Firmware
│   ├── main.py                 # Main application (enhanced)
│   ├── config.py               # Configuration settings
│   └── animations.py           # LED animation library
│
├── 🌐 web/                      # Web Control Panel
│   ├── index.html              # Main page
│   ├── styles.css              # Premium styling
│   └── app.js                  # MQTT client logic
│
├── 🔧 tools/                    # Development Tools
│   ├── desktop_simulator.py    # GUI simulator
│   └── mqtt_tester.py          # CLI testing tool
│
├── 🧪 tests/                    # Testing
│   ├── simulator_demo.py       # Wokwi simulator code
│   └── test_hardware.py        # Hardware test scripts
│
├── 📚 docs/                     # Documentation
│   └── setup_guide.md          # Detailed setup guide
│
├── 📄 README.md                 # This file
├── 📋 CONTRACT_TEMPLATE.html    # Development contract
└── 📝 CLIENT_CONSULTATION_CHECKLIST.md
```

---

## 🖥️ Desktop Simulator

Test the entire system without any Raspberry Pi hardware!

```bash
pip install paho-mqtt
python tools/desktop_simulator.py
```

**Features:**
- 🐋 Two visual whales with LED ring animations
- 📡 Real MQTT communication via HiveMQ
- 🎨 Color picker with presets
- 🌊 Multiple animation patterns
- 📋 Activity log

---

## 🌐 Web Control Panel

A beautiful, responsive web interface for controlling your whales from any device.

```bash
# Open in browser
open web/index.html
```

**Features:**
- 🎨 Ocean-themed dark UI with glassmorphism
- 🐋 Live whale status cards with LED visualization
- 🎨 Color picker with preset colors
- 🌊 8 animation patterns to choose from
- 📡 Real-time MQTT over WebSocket
- 📱 Mobile-responsive design

---

## 🔧 Hardware Requirements (Per Whale)

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Raspberry Pi Pico W | 1 | Main controller with WiFi |
| TTP223 Touch Sensor | 1 | Detect touch input |
| NeoPixel Ring (12 LEDs) | 1 | LED animations |
| USB Cable | 1 | Power supply |

**Minimum Setup:** Just Pico W + Touch Sensor (uses onboard LED)

### Wiring Diagram

```
TTP223 Touch Sensor:
  VCC  → Pico 3V3 (Pin 36)
  GND  → Pico GND (Pin 38)
  SIG  → Pico GPIO15 (Pin 20)

NeoPixel Ring (Optional):
  5V/VCC → Pico VBUS (Pin 40) or external 5V
  GND    → Pico GND
  DIN    → Pico GPIO16 (Pin 21)
```

---

## 🎨 Available Animation Patterns

| Pattern | Description |
|---------|-------------|
| `idle` | Dim blue waiting state |
| `solid` | Solid color at full brightness |
| `pulse` | Smooth pulsing brightness |
| `breathing` | Slow, calming breathing effect |
| `rainbow` | Color wheel rotation |
| `wave` | Wave pattern around ring |
| `sparkle` | Random white sparkles |
| `comet` | Shooting star effect |
| `fire` | Flickering candle effect |
| `ocean` | Blue-teal ocean waves |
| `celebration` | Party mode! |

---

## 📡 MQTT Communication

Uses free HiveMQ public broker - no server setup required!

**Broker:** `broker.hivemq.com`
**Port:** `1883` (TCP) | `8884` (WebSocket Secure)

### Topics

| Topic | Purpose |
|-------|---------|
| `pico_whale/{pair_id}/touch` | Touch events between whales |
| `pico_whale/{pair_id}/color` | LED color changes |
| `pico_whale/{pair_id}/pattern` | Animation pattern changes |
| `pico_whale/{pair_id}/heartbeat` | Online status |

### Testing with CLI

```bash
# Install
pip install paho-mqtt

# Interactive mode
python tools/mqtt_tester.py --interactive

# Commands in interactive mode:
#   1 - Touch whale_1
#   2 - Touch whale_2
#   c - Set color
#   p - Set pattern
```

---

## ⚙️ Configuration

Edit `src/config.py`:

```python
# WiFi Settings
WIFI_SSID = "YourWiFiName"
WIFI_PASSWORD = "YourPassword"

# Device Identity (DIFFERENT for each whale!)
DEVICE_ID = "whale_1"  # or "whale_2"

# Unique pair identifier
WHALE_PAIR_ID = "whale_pair_jeff_friend"

# Hardware
USE_NEOPIXEL = True      # Set to False for onboard LED only
NEOPIXEL_COUNT = 12      # Number of LEDs
```

---

## 🧪 Testing Tools

### MQTT Tester (Command Line)

```bash
# Subscribe and monitor all messages
python tools/mqtt_tester.py --subscribe

# Send a touch from whale_1
python tools/mqtt_tester.py --touch whale_1

# Change color
python tools/mqtt_tester.py --color 255,100,200

# Change pattern
python tools/mqtt_tester.py --pattern rainbow
```

### Wokwi Online Simulator

1. Go to [wokwi.com/projects/new/micropython-pi-pico-w](https://wokwi.com/projects/new/micropython-pi-pico-w)
2. Copy code from `tests/simulator_demo.py`
3. Add components: Push Button (GPIO15), NeoPixel Ring (GPIO16)
4. Run simulation!

---

## 🚀 Deployment Checklist

### Whale 1 (Your House)
- [ ] Flash MicroPython to Pico W
- [ ] Install `umqtt.simple` library
- [ ] Set `DEVICE_ID = "whale_1"`
- [ ] Enter your WiFi credentials
- [ ] Upload code via Pico-W-Go extension
- [ ] Test with desktop simulator

### Whale 2 (Friend's House)
- [ ] Flash MicroPython to second Pico W
- [ ] Install `umqtt.simple` library
- [ ] Set `DEVICE_ID = "whale_2"`
- [ ] Enter friend's WiFi credentials
- [ ] Upload code
- [ ] Give to friend - just plug in!

---

## 🐛 Troubleshooting

### WiFi Issues
- Check SSID and password (case-sensitive!)
- Pico W only supports 2.4GHz WiFi (not 5GHz)
- Check router is in range

### MQTT Issues
- Verify internet connection
- Check firewall (port 1883/8884)
- Use `mqtt_tester.py` to debug

### Touch Sensor Issues
```python
# Test touch sensor only
from machine import Pin
touch = Pin(15, Pin.IN, Pin.PULL_DOWN)
while True:
    print(touch.value())
    time.sleep(0.5)
```

### LED Issues
```python
# Test NeoPixels only
from machine import Pin
import neopixel
np = neopixel.NeoPixel(Pin(16), 12)
np[0] = (255, 0, 0)  # Red
np.write()
```

---

## 📝 Development Notes

### Time Estimates
- Core firmware: ✅ Complete (~8-12 hours)
- Animation library: ✅ Complete (~4 hours)
- Desktop simulator: ✅ Complete (~6 hours)
- Web control panel: ✅ Complete (~8 hours)
- Documentation: ✅ Complete (~3 hours)

### Technology Stack
- **Firmware:** MicroPython
- **Communication:** MQTT (HiveMQ broker)
- **Desktop GUI:** Python + Tkinter
- **Web Panel:** HTML/CSS/JavaScript + MQTT.js
- **Animations:** Custom Python library

---

## 📄 License

MIT License - Feel free to use and modify!

---

## 🤝 Credits

Built with ❤️ for connected friends who want to stay close across any distance.

---

## 📞 Support

For issues or questions, check the troubleshooting section above or open an issue on GitHub.
