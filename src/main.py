# Pico Whale Project - Enhanced Main Application
# ================================================
# Production-ready firmware with multiple animation patterns,
# heartbeat system, and improved error recovery.
# Works with just Pico W onboard LED, Servo, Sound Sensor, or NeoPixel strip.

import math

import time
import network
import json
from machine import Pin, PWM, ADC

# Import configuration
from config import (
    WIFI_SSID, WIFI_PASSWORD,
    MQTT_BROKER, MQTT_PORT,
    TOPIC_TOUCH, TOPIC_HEARTBEAT, TOPIC_COLOR, TOPIC_PATTERN,
    WHALE_PAIR_ID, DEVICE_ID,
    TOUCH_SENSOR_PIN,
    USE_NEOPIXEL, NEOPIXEL_PIN, NEOPIXEL_COUNT,
    COLOR_TOUCHED, COLOR_IDLE,
    RESPONSE_DURATION, TOUCH_COOLDOWN, HEARTBEAT_INTERVAL,
    USE_SERVO, SERVO_PIN, USE_SOUND_SENSOR, SOUND_SENSOR_PIN
)

# Import animations
try:
    from animations import AnimationLibrary, run_pattern
    ANIMATIONS_AVAILABLE = True
except ImportError:
    ANIMATIONS_AVAILABLE = False
    print("Note: animations.py not found - using basic animations")

# Only import neopixel if we're using it
if USE_NEOPIXEL:
    import neopixel

# Try to import umqtt
try:
    from umqtt.simple import MQTTClient
    MQTT_AVAILABLE = True
except ImportError:
    print("WARNING: umqtt not found. Running in demo mode.")
    print("Install with: import mip; mip.install('umqtt.simple')")
    MQTT_AVAILABLE = False


class PicoWhale:
    """Main class for the connected whale device with enhanced features."""
    
    def __init__(self):
        print("Initializing Pico Whale...")
        
        # Onboard LED (always available)
        self.onboard_led = Pin("LED", Pin.OUT)
        
        # Touch sensor
        self.touch_sensor = Pin(TOUCH_SENSOR_PIN, Pin.IN, Pin.PULL_DOWN)
        
        # Optional NeoPixel LEDs
        if USE_NEOPIXEL:
            self.leds = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT)
            print(f"  NeoPixel enabled: {NEOPIXEL_COUNT} LEDs on GPIO{NEOPIXEL_PIN}")
        else:
            self.leds = None
            print("  Using onboard LED only")
        
        # Optional Servo
        if USE_SERVO:
            self.servo = PWM(Pin(SERVO_PIN))
            self.servo.freq(50)
            print(f"  Servo enabled on GPIO{SERVO_PIN}")
        else:
            self.servo = None

        # Optional Sound Sensor
        if USE_SOUND_SENSOR:
            self.sound_sensor = Pin(SOUND_SENSOR_PIN, Pin.IN)
            print(f"  Sound sensor enabled on GPIO{SOUND_SENSOR_PIN}")
        else:
            self.sound_sensor = None

        # Animation library
        if ANIMATIONS_AVAILABLE and USE_NEOPIXEL:
            self.animator = AnimationLibrary(NEOPIXEL_COUNT)
            self.animator.set_color(COLOR_TOUCHED[0], COLOR_TOUCHED[1], COLOR_TOUCHED[2])
        else:
            self.animator = None
        
        # State tracking
        self.connected = False
        self.wifi_connected = False
        self.last_touch_time = 0
        self.last_heartbeat_time = 0
        self.responding = False
        self.response_end_time = 0
        self.current_pattern = "pulse"
        self.current_color = COLOR_TOUCHED
        
        # MQTT client
        self.mqtt = None
        
        # Network
        self.wlan = None
        
        # Statistics
        self.touch_count = 0
        self.received_count = 0
        self.reconnect_count = 0
        
        print("  Hardware initialized!")
    
    # =========================================================================
    # Network & MQTT
    # =========================================================================
    
    def connect_wifi(self) -> bool:
        """Connect to WiFi network with retry logic."""
        print(f"\nConnecting to WiFi: {WIFI_SSID}")
        self.blink_status(2)  # 2 blinks = connecting
        
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
        # Check if already connected
        if self.wlan.isconnected():
            self.wifi_connected = True
            print(f"  ✓ Already connected! IP: {self.wlan.ifconfig()[0]}")
            return True
        
        self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection with timeout
        max_wait = 30
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print(f"  Waiting... ({max_wait}s remaining)")
            self.onboard_led.toggle()
            time.sleep(1)
        
        if self.wlan.status() != 3:
            print("  ✗ Failed to connect to WiFi!")
            self.blink_error()
            self.wifi_connected = False
            return False
        
        self.wifi_connected = True
        print(f"  ✓ Connected! IP: {self.wlan.ifconfig()[0]}")
        self.blink_status(3)
        return True
    
    def check_wifi(self) -> bool:
        """Check WiFi connection and reconnect if needed."""
        if self.wlan is None:
            return False
        
        if not self.wlan.isconnected():
            self.wifi_connected = False
            self.connected = False
            print("WiFi disconnected, attempting reconnect...")
            self.reconnect_count += 1
            return self.connect_wifi()
        
        return True
    
    def connect_mqtt(self) -> bool:
        """Connect to MQTT broker with error handling."""
        if not MQTT_AVAILABLE:
            print("MQTT not available - running in local demo mode")
            return False
        
        print(f"\nConnecting to MQTT: {MQTT_BROKER}")
        
        try:
            # Pre-connection check to avoid hanging forever if port is blocked
            import socket
            print(f"  Checking broker {MQTT_BROKER}:{MQTT_PORT}...")
            s = socket.socket()
            s.settimeout(5)
            try:
                addr = socket.getaddrinfo(MQTT_BROKER, MQTT_PORT)[0][-1]
                s.connect(addr)
                s.close()
                print("  ✓ Broker port is open")
            except Exception as e:
                print(f"  ✗ MQTT port {MQTT_PORT} blocked or unreachable: {e}")
                return False

            client_id = f"whale_{DEVICE_ID}_{int(time.time()) %10000}"
                
            self.mqtt = MQTTClient(
                client_id=client_id,
                server=MQTT_BROKER,
                port=MQTT_PORT,
                keepalive=60,
                ssl=(MQTT_PORT == 8883)
            )
            self.mqtt.set_callback(self.on_message)
            
            # Increase socket timeout for slow SSL handshake
            self.mqtt.connect(timeout=20)
            
            # Subscribe to topics
            self.mqtt.subscribe(TOPIC_TOUCH)
            self.mqtt.subscribe(TOPIC_COLOR)
            self.mqtt.subscribe(TOPIC_PATTERN)
            
            self.connected = True
            print("  ✓ MQTT connected and subscribed!")
            
            # Send online status
            self.send_heartbeat()
            return True
            
        except Exception as e:
            print(f"  ✗ MQTT connection failed: {e}")
            self.connected = False
            return False
    
    def check_mqtt(self) -> bool:
        """Check MQTT connection and reconnect if needed."""
        if not self.connected or self.mqtt is None:
            return self.connect_mqtt()
        
        try:
            # Try to ping or do a simple operation
            self.mqtt.ping()
            return True
        except:
            print("MQTT connection lost, reconnecting...")
            self.connected = False
            self.reconnect_count += 1
            return self.connect_mqtt()
    
    # =========================================================================
    # Message Handling
    # =========================================================================
    
    def on_message(self, topic, msg):
        """Handle incoming MQTT messages."""
        topic_str = topic.decode() if isinstance(topic, bytes) else topic
        message = msg.decode() if isinstance(msg, bytes) else msg
        
        print(f"\n>> Received on {topic_str.split('/')[-1]}: {message}")
        
        # Handle touch messages
        if "touch" in topic_str:
            # Ignore our own messages
            if message.startswith(DEVICE_ID):
                print("   (Ignoring own message)")
                return
            
            # Another whale was touched!
            self.received_count += 1
            print(f"🐋 Your friend touched their whale! (#{self.received_count})")
            self.start_response()
        
        # Handle color messages
        elif "color" in topic_str:
            try:
                parts = message.split(",")
                if len(parts) == 3:
                    r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                    self.current_color = (r, g, b)
                    if self.animator:
                        self.animator.set_color(r, g, b)
                    print(f"🎨 Color changed to RGB({r},{g},{b})")
            except Exception as e:
                print(f"   Color parse error: {e}")
        
        # Handle pattern messages
        elif "pattern" in topic_str:
            self.current_pattern = message
            print(f"🌊 Pattern changed to: {message}")
    
    # =========================================================================
    # Touch & Response
    # =========================================================================
    
    def start_response(self):
        """Start the response animation - whale was activated!"""
        self.responding = True
        self.response_end_time = time.time() + RESPONSE_DURATION
        print(f"   Responding for {RESPONSE_DURATION} seconds...")
    
    def send_touch(self):
        """Send a touch event to the other whale(s)."""
        self.touch_count += 1
        
        if not self.connected:
            print("Not connected - simulating local touch")
            self.start_response()
            return
        
        try:
            message = f"{DEVICE_ID}:touch:{int(time.time())}"
            self.mqtt.publish(TOPIC_TOUCH, message)
            print(f"\n<< Sent touch signal! 🐋 (#{self.touch_count})")
            
            # Quick flash to confirm send
            self.onboard_led.on()
            time.sleep(0.1)
            self.onboard_led.off()
            
        except Exception as e:
            print(f"Error sending touch: {e}")
            self.connected = False
    
    def send_heartbeat(self):
        """Send heartbeat to indicate online status."""
        if not self.connected or self.mqtt is None:
            return
        
        try:
            heartbeat = json.dumps({
                "device": DEVICE_ID,
                "status": "online",
                "uptime": time.time(),
                "touch_count": self.touch_count,
                "received_count": self.received_count,
                "pattern": self.current_pattern
            })
            
            topic = f"pico_whale/{WHALE_PAIR_ID}/heartbeat"
            self.mqtt.publish(topic, heartbeat)
            self.last_heartbeat_time = time.time()
            
        except Exception as e:
            print(f"Heartbeat error: {e}")
    
    # =========================================================================
    # LED Control
    # =========================================================================
    
    def set_leds(self, on=True):
        """Control the LED(s) - works with onboard LED or NeoPixels."""
        if on:
            self.onboard_led.on()
            if self.leds:
                for i in range(NEOPIXEL_COUNT):
                    self.leds[i] = self.current_color
                self.leds.write()
        else:
            self.onboard_led.off()
            if self.leds:
                for i in range(NEOPIXEL_COUNT):
                    self.leds[i] = (0, 0, 0)
                self.leds.write()
    
    def animate_response(self):
        """Animate the LED(s) during response."""
        # Use animation library if available
        if self.animator and self.leds:
            colors = run_pattern(self.animator, self.current_pattern)
            for i, color in enumerate(colors):
                if i < NEOPIXEL_COUNT:
                    self.leds[i] = color
            self.leds.write()
            
            # Also blink onboard LED
            self.onboard_led.value((int(time.time() * 3) % 2))
        else:
            # Simple on/off blink for onboard LED
            t = time.ticks_ms()
            on = (t // 300) % 2 == 0
            self.onboard_led.value(on)
            
            if self.leds:
                brightness = 0.5 + 0.5 * ((t % 1000) / 1000)
                r = int(self.current_color[0] * brightness)
                g = int(self.current_color[1] * brightness)
                b = int(self.current_color[2] * brightness)
                for i in range(NEOPIXEL_COUNT):
                    self.leds[i] = (r, g, b)
                self.leds.write()

        # Servo "Tail Flapp" movement during response
        if self.servo:
            # Create a waving movement based on time
            t = time.ticks_ms()
            angle_speed = 10 # frequency of flap
            # Calculate duty cycle for servo (roughly 0 to 180 degrees)
            # Standard servos use 1ms-2ms pulses at 50Hz
            # On Pico: duty_u16 range is 0-65535. 50Hz period is 20ms.
            # 1ms = 5% duty = 3276
            # 2ms = 10% duty = 6553
            angle = (math.sin(t / 100) + 1) / 2 # 0.0 to 1.0
            duty = int(3276 + (angle * 3277))
            self.servo.duty_u16(duty)
    
    def show_idle(self):
        """Show idle state on LEDs."""
        if self.leds:
            for i in range(NEOPIXEL_COUNT):
                self.leds[i] = COLOR_IDLE
            self.leds.write()
        self.onboard_led.off()
    
    # =========================================================================
    # Status Indicators
    # =========================================================================
    
    def blink_status(self, count):
        """Blink the onboard LED to indicate status."""
        for _ in range(count):
            self.onboard_led.on()
            time.sleep(0.15)
            self.onboard_led.off()
            time.sleep(0.15)
    
    def blink_error(self):
        """Rapid blink to indicate error."""
        for _ in range(10):
            self.onboard_led.on()
            time.sleep(0.1)
            self.onboard_led.off()
            time.sleep(0.1)
    
    # =========================================================================
    # Main Loop
    # =========================================================================
    
    def run(self):
        """Main application loop."""
        print()
        print("=" * 50)
        print("  🐋 PICO WHALE STARTING UP! 🐋")
        print("=" * 50)
        print(f"  Device ID: {DEVICE_ID}")
        print(f"  Touch Pin: GPIO{TOUCH_SENSOR_PIN}")
        print(f"  NeoPixels: {'Yes' if USE_NEOPIXEL else 'No (using onboard LED)'}")
        print(f"  Animations: {'Yes' if ANIMATIONS_AVAILABLE else 'Basic mode'}")
        print("=" * 50)
        
        # Connect to WiFi
        if not self.connect_wifi():
            print("\n⚠ WiFi failed - running in offline demo mode")
            print("  Touch the sensor to test LED response")
        else:
            # Connect to MQTT
            if not self.connect_mqtt():
                print("\n⚠ MQTT failed - running in offline demo mode")
        
        # Ready indicator
        print("\n" + "=" * 50)
        print("  ✓ READY! Touch the whale to send a signal")
        print("=" * 50 + "\n")
        self.blink_status(5)  # 5 blinks = ready!
        
        # Show idle pattern
        self.show_idle()
        
        # Main loop
        loop_count = 0
        while True:
            try:
                loop_count += 1
                current_time = time.time()
                
                # Check connections periodically (every ~10 seconds)
                if loop_count % 200 == 0:
                    self.check_wifi()
                    self.check_mqtt()
                
                # Check for incoming MQTT messages
                if self.connected and self.mqtt:
                    try:
                        self.mqtt.check_msg()
                    except Exception as e:
                        print(f"MQTT check error: {e}")
                        self.connected = False
                
                # Check touch sensor
                if self.touch_sensor.value() == 1:
                    if current_time - self.last_touch_time > TOUCH_COOLDOWN:
                        self.last_touch_time = current_time
                        print("Touch detected!")
                        self.send_touch()

                # Check Sound sensor (treat as touch)
                if self.sound_sensor and self.sound_sensor.value() == 1:
                    if current_time - self.last_touch_time > TOUCH_COOLDOWN:
                        self.last_touch_time = current_time
                        print("Sound detected!")
                        self.send_touch()
                
                # Handle response animation
                if self.responding:
                    if current_time > self.response_end_time:
                        # Response finished
                        self.responding = False
                        self.show_idle()
                        print("Response complete.\n")
                    else:
                        # Continue animation
                        self.animate_response()
                
                # Send heartbeat periodically
                if current_time - self.last_heartbeat_time > HEARTBEAT_INTERVAL:
                    self.send_heartbeat()
                
                time.sleep(0.05)  # 20 FPS
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.set_leds(False)
                if self.mqtt:
                    try:
                        # Send offline status
                        offline = json.dumps({
                            "device": DEVICE_ID,
                            "status": "offline",
                            "timestamp": int(time.time())
                        })
                        self.mqtt.publish(f"pico_whale/{WHALE_PAIR_ID}/heartbeat", offline)
                        self.mqtt.disconnect()
                    except:
                        pass
                break
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.blink_error()
                time.sleep(1)


# Need to define WHALE_PAIR_ID from config
try:
    from config import WHALE_PAIR_ID
except ImportError:
    WHALE_PAIR_ID = "whale_pair_jeff_friend"


# Entry point
if __name__ == "__main__":
    whale = PicoWhale()
    whale.run()
