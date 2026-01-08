# Hardware Test Script for Pico Whale
# ====================================
# Run this file to test each component individually

from machine import Pin
import neopixel
import time

# Pin assignments (match your config.py)
TOUCH_PIN = 15
NEOPIXEL_PIN = 16
NEOPIXEL_COUNT = 12
VIBRATION_PIN = 17


def test_led():
    """Test the NeoPixel LEDs."""
    print("=" * 40)
    print("Testing NeoPixel LEDs")
    print("=" * 40)
    
    np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT)
    
    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("White", (255, 255, 255)),
        ("Off", (0, 0, 0)),
    ]
    
    for name, color in colors:
        print(f"  Color: {name}")
        for i in range(NEOPIXEL_COUNT):
            np[i] = color
        np.write()
        time.sleep(1)
    
    # Rainbow cycle
    print("  Rainbow animation...")
    for _ in range(2):  # 2 cycles
        for j in range(256):
            for i in range(NEOPIXEL_COUNT):
                pixel_index = (i * 256 // NEOPIXEL_COUNT) + j
                np[i] = wheel(pixel_index & 255)
            np.write()
            time.sleep(0.01)
    
    # Turn off
    for i in range(NEOPIXEL_COUNT):
        np[i] = (0, 0, 0)
    np.write()
    
    print("✓ LED test complete!")
    print()


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)


def test_touch():
    """Test the touch sensor."""
    print("=" * 40)
    print("Testing Touch Sensor")
    print("=" * 40)
    print("Touch the sensor... (10 second test)")
    print()
    
    touch = Pin(TOUCH_PIN, Pin.IN, Pin.PULL_DOWN)
    led = Pin("LED", Pin.OUT)  # Built-in LED
    
    start_time = time.time()
    touch_count = 0
    last_state = 0
    
    while time.time() - start_time < 10:
        state = touch.value()
        
        if state == 1 and last_state == 0:
            touch_count += 1
            print(f"  Touch detected! (Count: {touch_count})")
            led.on()
        elif state == 0 and last_state == 1:
            led.off()
        
        last_state = state
        time.sleep(0.05)
    
    led.off()
    print(f"✓ Touch test complete! Total touches: {touch_count}")
    print()


def test_vibration():
    """Test the vibration motor."""
    print("=" * 40)
    print("Testing Vibration Motor")
    print("=" * 40)
    
    try:
        motor = Pin(VIBRATION_PIN, Pin.OUT)
        
        patterns = [
            ("Short pulse", [(0.1, 1), (0.1, 0)]),
            ("Long pulse", [(0.5, 1), (0.2, 0)]),
            ("Pattern", [(0.1, 1), (0.1, 0), (0.1, 1), (0.1, 0), (0.3, 1), (0.2, 0)]),
        ]
        
        for name, pattern in patterns:
            print(f"  Pattern: {name}")
            for duration, state in pattern:
                if state:
                    motor.on()
                else:
                    motor.off()
                time.sleep(duration)
            motor.off()
            time.sleep(0.5)
        
        print("✓ Vibration test complete!")
        
    except Exception as e:
        print(f"⚠ Vibration motor not available: {e}")
    
    print()


def test_wifi():
    """Test WiFi connection."""
    print("=" * 40)
    print("Testing WiFi Connection")
    print("=" * 40)
    
    import network
    
    # You can hardcode these for testing or import from config
    SSID = "YOUR_WIFI_NAME"
    PASSWORD = "YOUR_WIFI_PASSWORD"
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    print(f"  Scanning for networks...")
    networks = wlan.scan()
    print(f"  Found {len(networks)} networks:")
    for net in networks[:5]:  # Show first 5
        print(f"    - {net[0].decode()}")
    
    if SSID != "YOUR_WIFI_NAME":
        print(f"\n  Connecting to {SSID}...")
        wlan.connect(SSID, PASSWORD)
        
        timeout = 10
        while timeout > 0 and not wlan.isconnected():
            print(f"    Waiting... ({timeout}s)")
            time.sleep(1)
            timeout -= 1
        
        if wlan.isconnected():
            print(f"  ✓ Connected! IP: {wlan.ifconfig()[0]}")
        else:
            print("  ✗ Connection failed!")
    else:
        print("\n  ⚠ Update SSID/PASSWORD in this file to test connection")
    
    print()


def run_all_tests():
    """Run all hardware tests."""
    print()
    print("╔════════════════════════════════════════╗")
    print("║   PICO WHALE HARDWARE TEST SUITE       ║")
    print("╚════════════════════════════════════════╝")
    print()
    
    test_led()
    test_touch()
    test_vibration()
    test_wifi()
    
    print("╔════════════════════════════════════════╗")
    print("║   ALL TESTS COMPLETE!                  ║")
    print("╚════════════════════════════════════════╝")
    print()
    print("If any tests failed, check:")
    print("  1. Wiring connections")
    print("  2. Pin assignments in this file")
    print("  3. Component power supply")


# Run tests when this file is executed
if __name__ == "__main__":
    run_all_tests()
