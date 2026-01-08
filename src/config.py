# Pico Whale Project - Configuration
# ====================================
# Edit these settings for your specific setup
# IMPORTANT: Each whale device needs a DIFFERENT DEVICE_ID!

# ===========================================
# WiFi Configuration
# ===========================================
# Your home WiFi network credentials
WIFI_SSID = "Jeff Goldner’s iPhone"
WIFI_PASSWORD = "Hunter777"

# ===========================================
# MQTT Broker Configuration
# ===========================================
# Using test.mosquitto.org - reliable public broker
# Alternative: broker.hivemq.com or broker.emqx.io
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

# Unique identifier for your whale pair
# Change this to something unique to avoid conflicts with others!
WHALE_PAIR_ID = "whale_pair_jeff_friend"

# MQTT Topics (automatically generated from pair ID)
TOPIC_TOUCH = f"pico_whale/{WHALE_PAIR_ID}/touch"
TOPIC_HEARTBEAT = f"pico_whale/{WHALE_PAIR_ID}/heartbeat"
TOPIC_COLOR = f"pico_whale/{WHALE_PAIR_ID}/color"
TOPIC_PATTERN = f"pico_whale/{WHALE_PAIR_ID}/pattern"
TOPIC_STATUS = f"pico_whale/{WHALE_PAIR_ID}/status"

# ===========================================
# Device Identity
# ===========================================
# IMPORTANT: Set this differently for each whale!
# Options: "whale_1" or "whale_2"
# Whale 1 = Your house
# Whale 2 = Friend's house
DEVICE_ID = "whale_1"

# ===========================================
# Hardware Pin Configuration
# ===========================================
# Touch sensor GPIO pin
# TTP223 SIG output connects to this pin
TOUCH_SENSOR_PIN = 15  # GPIO15 (Pin 20 on the board)

# ===========================================
# LED Configuration
# ===========================================
# Set to False to use ONLY the onboard LED (no extra hardware needed!)
# Set to True if you have a NeoPixel strip/ring connected
USE_NEOPIXEL = False

# NeoPixel settings (only used if USE_NEOPIXEL = True)
NEOPIXEL_PIN = 16          # GPIO pin for NeoPixel data line
NEOPIXEL_COUNT = 12        # Number of LEDs in your ring/strip

# ===========================================
# Servo & Sound Configuration (New Hardware!)
# ===========================================
# Servo Motor (for tail flapping)
USE_SERVO = True
SERVO_PIN = 17             # GPIO pin for Servo signal

# Sound Sensor (detects claps or loud noises)
USE_SOUND_SENSOR = True
SOUND_SENSOR_PIN = 14      # GPIO pin for Sound Sensor digital output

# LED Colors (RGB format, 0-255) - default values
COLOR_IDLE = (10, 30, 60)          # Dim blue when idle/waiting
COLOR_TOUCHED = (255, 100, 200)    # Pink/purple when activated
COLOR_SENDING = (100, 255, 100)    # Green flash when you touch
COLOR_OFFLINE = (255, 50, 0)       # Orange/red when disconnected
COLOR_CONNECTED = (0, 255, 100)    # Green when connected

# ===========================================
# Behavior Settings
# ===========================================
# How long to light up when receiving a touch (seconds)
RESPONSE_DURATION = 5

# How often to send "I'm alive" signal (seconds)
HEARTBEAT_INTERVAL = 30

# Minimum seconds between touch detections (debounce)
TOUCH_COOLDOWN = 2

# Default animation pattern
DEFAULT_PATTERN = "pulse"

# ===========================================
# Advanced Settings
# ===========================================
# WiFi connection timeout (seconds)
WIFI_TIMEOUT = 30

# MQTT keepalive interval (seconds)
MQTT_KEEPALIVE = 60

# Enable debug messages
DEBUG_MODE = True


# ===========================================
# Quick Reference: Wiring Guide
# ===========================================
# 
# MINIMUM SETUP (onboard LED only):
#   TTP223 VCC  → Pico 3V3 (Pin 36)
#   TTP223 GND  → Pico GND (Pin 38)
#   TTP223 SIG  → Pico GPIO15 (Pin 20)
#
# WITH NEOPIXEL RING:
#   NeoPixel 5V/VCC → Pico VBUS (Pin 40) or external 5V
#   NeoPixel GND    → Pico GND
#   NeoPixel DIN    → Pico GPIO16 (Pin 21)
#
# ===========================================


# ===========================================
# Color Presets (for reference)
# ===========================================
# Use these as starting points for customization
COLOR_PRESETS = {
    "pink": (255, 100, 200),
    "cyan": (0, 212, 255),
    "green": (0, 255, 136),
    "orange": (255, 165, 0),
    "red": (255, 68, 68),
    "purple": (170, 0, 255),
    "white": (255, 255, 255),
    "warm_white": (255, 244, 229),
    "ocean": (0, 119, 190),
    "sunset": (255, 99, 71),
}
