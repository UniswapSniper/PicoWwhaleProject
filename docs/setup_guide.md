# 🚀 Complete Setup Guide

## Step 1: Install VS Code Extensions

### Required Extension: Pico-W-Go

1. Open VS Code
2. Press `Cmd+Shift+X` to open Extensions
3. Search for "**Pico-W-Go**"
4. Click Install

Alternative: Search for "**MicroPython**" by Microsoft

### What These Extensions Do:
- Connect to your Pico W over USB
- Upload Python files to the Pico
- Access the REPL (interactive Python shell)
- Debug and monitor your code

## Step 2: Install MicroPython on Pico W

### Download MicroPython Firmware

1. Go to: https://micropython.org/download/rp2-pico-w/
2. Download the latest `.uf2` file (e.g., `rp2-pico-w-20240105-v1.22.1.uf2`)

### Flash to Pico W

1. **Hold the BOOTSEL button** on your Pico W (small white button)
2. While holding, plug in the USB cable to your Mac
3. Release the button after connecting
4. A drive called `RPI-RP2` should appear on your desktop
5. Drag the `.uf2` file onto the `RPI-RP2` drive
6. The Pico will reboot automatically - the drive will disappear

### Verify Installation

1. In VS Code, open Command Palette (`Cmd+Shift+P`)
2. Type "Pico-W-Go: Connect" and select it
3. In the terminal at the bottom, you should see:
   ```
   MicroPython v1.22.1 on 2024-01-05; Raspberry Pi Pico W with RP2040
   Type "help()" for more information.
   >>> 
   ```

## Step 3: Install Required MicroPython Libraries

### Connect to REPL

1. Connect your Pico W via USB
2. In VS Code, run "Pico-W-Go: Connect"
3. You should see the `>>>` prompt

### Install umqtt Library

Type these commands in the REPL:

```python
import network
import mip

# Connect to WiFi first
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YOUR_WIFI_NAME", "YOUR_WIFI_PASSWORD")

# Wait for connection
import time
while not wlan.isconnected():
    print("Connecting...")
    time.sleep(1)
    
print("Connected!")

# Install umqtt library
mip.install("umqtt.simple")
print("Done!")
```

## Step 4: Configure Your Whale

### Edit config.py

1. Open `/src/config.py` in VS Code
2. Update these settings:

```python
# YOUR WiFi credentials
WIFI_SSID = "YourWiFiName"
WIFI_PASSWORD = "YourWiFiPassword"

# Unique ID for your whale pair
WHALE_PAIR_ID = "jeff_and_friend_whales"

# IMPORTANT: Set different for each whale!
# Whale 1 (your house):
DEVICE_ID = "whale_1"

# Whale 2 (friend's house):
DEVICE_ID = "whale_2"
```

## Step 5: Upload Code to Pico W

### Using Pico-W-Go

1. Open the project folder in VS Code
2. Connect Pico W via USB
3. Run "Pico-W-Go: Connect"
4. Navigate to the `src/` folder
5. Right-click and select "**Pico-W-Go: Upload project**"

Or manually:
1. Open Command Palette (`Cmd+Shift+P`)
2. Run "**Pico-W-Go: Upload current file**" for each file

### File Structure on Pico

After upload, your Pico should have:
```
/
├── main.py          # Runs automatically on boot
├── config.py        # Your settings
└── lib/
    └── umqtt/
        └── simple.py
```

## Step 6: Test Your Whale

### Basic Test

1. With Pico connected, open the terminal (REPL)
2. You should see startup messages:
   ```
   ========================================
   🐋 Pico Whale Starting Up!
   Device ID: whale_1
   ========================================
   Connecting to WiFi: YourWiFi
   Connected! IP: 192.168.1.xxx
   Connecting to MQTT broker: broker.hivemq.com
   MQTT connected! Subscribed to: pico_whale/...
   Ready! Touch the whale to send a signal.
   ```

### Test Touch Sensor

1. Touch the sensor
2. You should see in terminal:
   ```
   Sent touch signal! 🐋
   ```

## Step 7: Test Communication

### Using Two Picos

1. Set up both Picos with different `DEVICE_ID` values
2. Power them both on
3. Touch whale_1 → whale_2 should light up
4. Touch whale_2 → whale_1 should light up

### Testing with One Pico

You can use an MQTT client on your computer:

1. Install an MQTT client (like MQTT Explorer)
2. Connect to `broker.hivemq.com:1883`
3. Subscribe to `pico_whale/your_pair_id/touch`
4. Send a test message to see your whale respond

## Step 8: Deploy to Friend's House

### Prepare Whale 2

1. Flash second Pico W with MicroPython
2. Install umqtt library
3. Update `config.py`:
   - Same `WHALE_PAIR_ID` as whale 1
   - `DEVICE_ID = "whale_2"`
   - Friend's WiFi credentials
4. Upload code to Pico

### Give to Friend

- They just need to plug in the USB and it will auto-connect!
- Make sure they have WiFi at their location

## Troubleshooting

### "Cannot connect to Pico"
- Make sure no other program is using the serial port
- Unplug and replug the USB cable
- Try a different USB cable (some are charge-only)

### "WiFi connection failed"
- Double-check SSID and password (case-sensitive!)
- Make sure Pico is within range of router
- Check if your WiFi is 2.4GHz (Pico doesn't support 5GHz)

### "MQTT connection failed"
- Check internet connection
- Try a different broker
- Firewall may be blocking port 1883

### "Touch sensor not responding"
- Check wiring connections
- Test sensor with simple code:
  ```python
  from machine import Pin
  import time
  
  touch = Pin(15, Pin.IN, Pin.PULL_DOWN)
  while True:
      print(touch.value())
      time.sleep(0.5)
  ```

### "LEDs not working"
- Check power supply (NeoPixels need good power)
- Verify data pin connection
- Test with simple code:
  ```python
  from machine import Pin
  import neopixel
  
  np = neopixel.NeoPixel(Pin(16), 12)
  np[0] = (255, 0, 0)  # Red
  np.write()
  ```

## Next Steps

1. ✅ Get basic setup working
2. 🐋 Install in whale figures
3. 🎨 Customize LED patterns
4. 🔊 Add sound (optional)
5. 📱 Create status webpage (optional)
