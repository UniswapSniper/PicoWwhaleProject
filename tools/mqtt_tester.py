#!/usr/bin/env python3
"""
🐋 MQTT Communication Tester
=============================
Command-line tool for testing MQTT communication with Pico Whale devices.

Requirements:
    pip install paho-mqtt

Usage:
    python mqtt_tester.py --subscribe       # Listen for messages
    python mqtt_tester.py --touch whale_1   # Simulate touch from whale_1
    python mqtt_tester.py --color 255,100,200  # Send color change
    python mqtt_tester.py --pattern rainbow # Send pattern change
"""

import argparse
import time
import sys
import json
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("❌ paho-mqtt not installed!")
    print("   Run: pip install paho-mqtt")
    sys.exit(1)


# Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
WHALE_PAIR_ID = "whale_pair_jeff_friend"

# Topics
TOPIC_TOUCH = f"pico_whale/{WHALE_PAIR_ID}/touch"
TOPIC_HEARTBEAT = f"pico_whale/{WHALE_PAIR_ID}/heartbeat"
TOPIC_COLOR = f"pico_whale/{WHALE_PAIR_ID}/color"
TOPIC_PATTERN = f"pico_whale/{WHALE_PAIR_ID}/pattern"
TOPIC_STATUS = f"pico_whale/{WHALE_PAIR_ID}/status"


class MQTTTester:
    """MQTT testing utility."""
    
    def __init__(self):
        self.client = mqtt.Client(client_id=f"tester_{int(time.time())}")
        self.connected = False
        
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        symbols = {
            "INFO": "ℹ️ ",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "RECEIVE": "📨",
            "SEND": "📤"
        }
        symbol = symbols.get(level, "  ")
        print(f"[{timestamp}] {symbol} {message}")
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self._log("Connected to MQTT broker", "SUCCESS")
            # Subscribe to all whale topics
            client.subscribe(f"pico_whale/{WHALE_PAIR_ID}/#")
            self._log(f"Subscribed to: pico_whale/{WHALE_PAIR_ID}/#")
        else:
            self._log(f"Connection failed with code: {rc}", "ERROR")
    
    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        topic_name = topic.split("/")[-1]
        self._log(f"[{topic_name}] {payload}", "RECEIVE")
    
    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        if rc != 0:
            self._log(f"Unexpected disconnection (rc={rc})", "ERROR")
    
    def connect(self):
        """Connect to the MQTT broker."""
        self._log(f"Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
            
            if not self.connected:
                self._log("Connection timeout", "ERROR")
                return False
            return True
        except Exception as e:
            self._log(f"Connection error: {e}", "ERROR")
            return False
    
    def disconnect(self):
        """Disconnect from broker."""
        self.client.loop_stop()
        self.client.disconnect()
        self._log("Disconnected")
    
    def send_touch(self, whale_id: str):
        """Send a touch signal."""
        message = f"{whale_id}:touch:{int(time.time())}"
        self.client.publish(TOPIC_TOUCH, message)
        self._log(f"Sent touch from {whale_id}", "SEND")
    
    def send_color(self, color_str: str):
        """Send a color change command."""
        self.client.publish(TOPIC_COLOR, color_str)
        self._log(f"Sent color: {color_str}", "SEND")
    
    def send_pattern(self, pattern: str):
        """Send a pattern change command."""
        self.client.publish(TOPIC_PATTERN, pattern)
        self._log(f"Sent pattern: {pattern}", "SEND")
    
    def send_heartbeat(self, whale_id: str):
        """Send a heartbeat signal."""
        message = json.dumps({
            "device": whale_id,
            "status": "online",
            "timestamp": int(time.time())
        })
        self.client.publish(TOPIC_HEARTBEAT, message)
        self._log(f"Sent heartbeat from {whale_id}", "SEND")
    
    def subscribe_loop(self):
        """Run subscription loop to monitor all messages."""
        self._log("Listening for messages... (Ctrl+C to stop)")
        print("-" * 50)
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n")
            self._log("Stopping listener...")
    
    def interactive_mode(self):
        """Run interactive command mode."""
        print("\n" + "=" * 50)
        print("  INTERACTIVE MODE")
        print("=" * 50)
        print("Commands:")
        print("  1 - Touch whale_1")
        print("  2 - Touch whale_2")
        print("  c - Set color (prompts for RGB)")
        print("  p - Set pattern (prompts for name)")
        print("  h - Send heartbeat")
        print("  q - Quit")
        print("=" * 50 + "\n")
        
        try:
            while True:
                cmd = input("Enter command: ").strip().lower()
                
                if cmd == "1":
                    self.send_touch("whale_1")
                elif cmd == "2":
                    self.send_touch("whale_2")
                elif cmd == "c":
                    color = input("Enter RGB (e.g., 255,100,200): ").strip()
                    self.send_color(color)
                elif cmd == "p":
                    print("Patterns: idle, solid, pulse, rainbow, wave, sparkle, breathing")
                    pattern = input("Enter pattern name: ").strip()
                    self.send_pattern(pattern)
                elif cmd == "h":
                    whale = input("Heartbeat from (whale_1/whale_2): ").strip()
                    self.send_heartbeat(whale)
                elif cmd == "q":
                    break
                else:
                    print("Unknown command")
                
                time.sleep(0.5)  # Brief pause to see responses
                
        except KeyboardInterrupt:
            pass


def main():
    parser = argparse.ArgumentParser(description="Pico Whale MQTT Tester")
    parser.add_argument("--subscribe", "-s", action="store_true",
                       help="Subscribe and listen for messages")
    parser.add_argument("--touch", "-t", type=str,
                       help="Send touch signal from specified whale (whale_1 or whale_2)")
    parser.add_argument("--color", "-c", type=str,
                       help="Send color change (format: R,G,B)")
    parser.add_argument("--pattern", "-p", type=str,
                       help="Send pattern change (idle, pulse, rainbow, wave, sparkle, breathing)")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    parser.add_argument("--broker", "-b", type=str, default=MQTT_BROKER,
                       help=f"MQTT broker address (default: {MQTT_BROKER})")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("  🐋 PICO WHALE MQTT TESTER")
    print("=" * 50)
    print(f"  Broker: {args.broker}")
    print(f"  Pair ID: {WHALE_PAIR_ID}")
    print("=" * 50 + "\n")
    
    tester = MQTTTester()
    
    if not tester.connect():
        sys.exit(1)
    
    try:
        if args.touch:
            tester.send_touch(args.touch)
            time.sleep(2)  # Wait to see response
        
        if args.color:
            tester.send_color(args.color)
            time.sleep(1)
        
        if args.pattern:
            tester.send_pattern(args.pattern)
            time.sleep(1)
        
        if args.interactive:
            tester.interactive_mode()
        elif args.subscribe:
            tester.subscribe_loop()
        elif not (args.touch or args.color or args.pattern):
            # Default to interactive if no specific action
            tester.interactive_mode()
            
    finally:
        tester.disconnect()


if __name__ == "__main__":
    main()
