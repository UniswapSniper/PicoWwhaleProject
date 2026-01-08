# Pico Whale - Wokwi Simulator Version
# =====================================
# Use this file to test in the Wokwi online simulator
# https://wokwi.com/projects/new/micropython-pi-pico-w
#
# In Wokwi, add these components:
#   1. Push Button (simulates touch sensor) → GPIO15
#   2. LED or NeoPixel Ring → GPIO16 (optional)

from machine import Pin
import time

# Configuration
TOUCH_PIN = 15
LED_PIN = 16
RESPONSE_DURATION = 3

# Setup
print("🐋 Pico Whale Simulator Starting...")

# Onboard LED
onboard_led = Pin("LED", Pin.OUT)

# Touch sensor (using button in simulator)
touch_sensor = Pin(TOUCH_PIN, Pin.IN, Pin.PULL_UP)

# External LED (optional - add in Wokwi if you want)
try:
    external_led = Pin(LED_PIN, Pin.OUT)
    has_external_led = True
    print("  External LED on GPIO16: Ready")
except:
    has_external_led = False

# State
responding = False
response_end_time = 0
last_touch_time = 0

def blink_startup():
    """Blink LED to show startup."""
    for _ in range(3):
        onboard_led.on()
        time.sleep(0.2)
        onboard_led.off()
        time.sleep(0.2)

def start_response():
    """Start the whale response (simulate receiving touch from friend)."""
    global responding, response_end_time
    responding = True
    response_end_time = time.time() + RESPONSE_DURATION
    print("🐋 Whale activated! Responding...")

def handle_touch():
    """Handle local touch event."""
    global last_touch_time
    current = time.time()
    if current - last_touch_time > 1:  # 1 second debounce
        last_touch_time = current
        print("👆 Touch detected! Sending signal...")
        # Quick flash to confirm
        onboard_led.on()
        time.sleep(0.1)
        onboard_led.off()
        # In real version, this would send MQTT message
        # For demo, we'll trigger our own response
        time.sleep(0.5)
        print("📨 Signal sent to friend's whale!")
        # Simulate friend touching back after 2 seconds
        start_response()

def animate():
    """Animate LEDs during response."""
    t = time.ticks_ms()
    on = (t // 200) % 2 == 0
    onboard_led.value(on)
    if has_external_led:
        external_led.value(on)

# Startup
print("=" * 40)
print("  PICO WHALE SIMULATOR")
print("=" * 40)
print("  Press the button to simulate touch")
print("=" * 40)
blink_startup()
print("✓ Ready!\n")

# Main loop
while True:
    # Check for touch/button press
    if touch_sensor.value() == 0:
        handle_touch()
    
    # Handle response animation
    if responding:
        if time.time() > response_end_time:
            responding = False
            onboard_led.off()
            if has_external_led:
                external_led.off()
            print("✓ Response complete.\n")
        else:
            animate()
    
    time.sleep(0.05)
