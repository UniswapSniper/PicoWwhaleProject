#!/usr/bin/env python3
"""
🐋 Pico Whale Desktop Simulator
================================
A visual simulator for testing the Pico Whale system without physical hardware.
Uses real MQTT communication via HiveMQ broker.

Requirements:
    pip install paho-mqtt

Usage:
    python desktop_simulator.py
"""

import tkinter as tk
from tkinter import ttk, colorchooser
import threading
import time
import math
import random
import json
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False
    print("⚠️  paho-mqtt not installed. Run: pip install paho-mqtt")
    print("   Running in offline demo mode...")


# =============================================================================
# Configuration
# =============================================================================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
WHALE_PAIR_ID = "whale_pair_jeff_friend"
TOPIC_TOUCH = f"pico_whale/{WHALE_PAIR_ID}/touch"
TOPIC_HEARTBEAT = f"pico_whale/{WHALE_PAIR_ID}/heartbeat"
TOPIC_COLOR = f"pico_whale/{WHALE_PAIR_ID}/color"
TOPIC_PATTERN = f"pico_whale/{WHALE_PAIR_ID}/pattern"

# Colors
COLOR_IDLE = "#0A1A2F"
COLOR_TOUCHED = "#FF64C8"
COLOR_CONNECTED = "#00FF88"
COLOR_DISCONNECTED = "#FF4444"
COLOR_OCEAN_BG = "#0A1628"
COLOR_PANEL_BG = "#0D2137"
COLOR_ACCENT = "#00D4FF"


# =============================================================================
# Animation Engine
# =============================================================================
class AnimationEngine:
    """Handles LED ring animations."""
    
    def __init__(self, num_leds=12):
        self.num_leds = num_leds
        self.current_pattern = "idle"
        self.base_color = (255, 100, 200)  # Pink/purple
        self.brightness = 1.0
        self.animation_offset = 0
        
    def get_led_colors(self) -> list:
        """Get current color for each LED based on pattern."""
        if self.current_pattern == "idle":
            return self._pattern_idle()
        elif self.current_pattern == "pulse":
            return self._pattern_pulse()
        elif self.current_pattern == "rainbow":
            return self._pattern_rainbow()
        elif self.current_pattern == "wave":
            return self._pattern_wave()
        elif self.current_pattern == "sparkle":
            return self._pattern_sparkle()
        elif self.current_pattern == "breathing":
            return self._pattern_breathing()
        elif self.current_pattern == "solid":
            return self._pattern_solid()
        else:
            return self._pattern_idle()
    
    def _pattern_idle(self) -> list:
        """Dim blue idle state."""
        return [(10, 30, 60)] * self.num_leds
    
    def _pattern_solid(self) -> list:
        """Solid color at current brightness."""
        r = int(self.base_color[0] * self.brightness)
        g = int(self.base_color[1] * self.brightness)
        b = int(self.base_color[2] * self.brightness)
        return [(r, g, b)] * self.num_leds
    
    def _pattern_pulse(self) -> list:
        """Pulsing brightness."""
        t = time.time() * 3
        brightness = 0.3 + 0.7 * abs(math.sin(t))
        r = int(self.base_color[0] * brightness)
        g = int(self.base_color[1] * brightness)
        b = int(self.base_color[2] * brightness)
        return [(r, g, b)] * self.num_leds
    
    def _pattern_rainbow(self) -> list:
        """Rainbow cycle around ring."""
        colors = []
        for i in range(self.num_leds):
            hue = (i / self.num_leds + self.animation_offset) % 1.0
            r, g, b = self._hsv_to_rgb(hue, 1.0, 1.0)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        self.animation_offset = (self.animation_offset + 0.01) % 1.0
        return colors
    
    def _pattern_wave(self) -> list:
        """Wave pattern around ring."""
        colors = []
        for i in range(self.num_leds):
            offset = (i / self.num_leds * 2 * math.pi) + (time.time() * 3)
            brightness = 0.3 + 0.7 * (math.sin(offset) + 1) / 2
            r = int(self.base_color[0] * brightness)
            g = int(self.base_color[1] * brightness)
            b = int(self.base_color[2] * brightness)
            colors.append((r, g, b))
        return colors
    
    def _pattern_sparkle(self) -> list:
        """Random sparkle effect."""
        colors = []
        for _ in range(self.num_leds):
            if random.random() < 0.15:  # 15% chance of sparkle
                colors.append((255, 255, 255))
            else:
                r = int(self.base_color[0] * 0.3)
                g = int(self.base_color[1] * 0.3)
                b = int(self.base_color[2] * 0.3)
                colors.append((r, g, b))
        return colors
    
    def _pattern_breathing(self) -> list:
        """Slow breathing glow."""
        t = time.time() * 0.5
        # Smooth breathing curve
        brightness = (math.exp(math.sin(t)) - 0.36787944) / 2.35040238
        r = int(self.base_color[0] * brightness)
        g = int(self.base_color[1] * brightness)
        b = int(self.base_color[2] * brightness)
        return [(r, g, b)] * self.num_leds
    
    @staticmethod
    def _hsv_to_rgb(h, s, v):
        """Convert HSV to RGB."""
        if s == 0.0:
            return (v, v, v)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)


# =============================================================================
# Whale Widget
# =============================================================================
class WhaleWidget(tk.Canvas):
    """Visual representation of a whale device with LED ring."""
    
    def __init__(self, parent, whale_id, on_touch_callback=None):
        super().__init__(parent, width=300, height=350, bg=COLOR_OCEAN_BG, 
                         highlightthickness=0)
        
        self.whale_id = whale_id
        self.on_touch = on_touch_callback
        self.animation = AnimationEngine(num_leds=12)
        self.responding = False
        self.response_end_time = 0
        
        # Draw initial state
        self._draw_base()
        self._draw_leds()
        
        # Bind click event
        self.bind("<Button-1>", self._on_click)
        
    def _draw_base(self):
        """Draw the whale base visualization."""
        # Outer glow ring
        self.create_oval(50, 50, 250, 250, outline=COLOR_ACCENT, width=2)
        
        # Whale emoji in center
        self.create_text(150, 140, text="🐋", font=("Arial", 64))
        
        # Device ID label
        self.create_text(150, 220, text=self.whale_id.replace("_", " ").title(),
                        font=("Helvetica", 14, "bold"), fill="white")
        
        # Touch prompt
        self.touch_text = self.create_text(150, 280, text="Click to touch",
                                           font=("Helvetica", 11), fill="#666")
        
        # Status indicator
        self.status_indicator = self.create_oval(140, 305, 160, 325, 
                                                  fill=COLOR_DISCONNECTED, 
                                                  outline="")
        self.status_text = self.create_text(150, 340, text="Offline",
                                            font=("Helvetica", 10), fill="#888")
        
        # LED positions (around the ring)
        self.led_items = []
        center_x, center_y = 150, 150
        radius = 90
        for i in range(12):
            angle = (i / 12) * 2 * math.pi - (math.pi / 2)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            led = self.create_oval(x-8, y-8, x+8, y+8, fill="#001122", outline="#003366")
            self.led_items.append(led)
    
    def _draw_leds(self):
        """Update LED colors."""
        colors = self.animation.get_led_colors()
        for i, led in enumerate(self.led_items):
            r, g, b = colors[i]
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.itemconfig(led, fill=color)
    
    def _on_click(self, event):
        """Handle touch/click event."""
        if self.on_touch:
            self.on_touch(self.whale_id)
    
    def set_status(self, connected: bool):
        """Update connection status display."""
        if connected:
            self.itemconfig(self.status_indicator, fill=COLOR_CONNECTED)
            self.itemconfig(self.status_text, text="Connected", fill=COLOR_CONNECTED)
        else:
            self.itemconfig(self.status_indicator, fill=COLOR_DISCONNECTED)
            self.itemconfig(self.status_text, text="Offline", fill=COLOR_DISCONNECTED)
    
    def start_response(self, duration=5):
        """Start response animation."""
        self.responding = True
        self.response_end_time = time.time() + duration
        self.animation.current_pattern = "pulse"
    
    def update_animation(self):
        """Update animation frame."""
        if self.responding:
            if time.time() > self.response_end_time:
                self.responding = False
                self.animation.current_pattern = "idle"
        self._draw_leds()
    
    def set_color(self, r, g, b):
        """Set the base LED color."""
        self.animation.base_color = (r, g, b)
    
    def set_pattern(self, pattern: str):
        """Set the animation pattern."""
        self.animation.current_pattern = pattern


# =============================================================================
# Main Application
# =============================================================================
class PicoWhaleSimulator:
    """Main desktop simulator application."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐋 Pico Whale Simulator")
        self.root.configure(bg=COLOR_OCEAN_BG)
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # MQTT client
        self.mqtt_client = None
        self.connected = False
        
        # Build UI
        self._create_ui()
        
        # Start MQTT connection
        if MQTT_AVAILABLE:
            self._connect_mqtt()
        
        # Start animation loop
        self._animation_loop()
        
    def _create_ui(self):
        """Build the user interface."""
        # Title bar
        title_frame = tk.Frame(self.root, bg=COLOR_PANEL_BG, height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🐋 Pico Whale Simulator", 
                              font=("Helvetica", 20, "bold"),
                              bg=COLOR_PANEL_BG, fg="white")
        title_label.pack(pady=15)
        
        # Connection status
        self.connection_label = tk.Label(title_frame, text="⚫ Connecting...",
                                        font=("Helvetica", 10),
                                        bg=COLOR_PANEL_BG, fg="#888")
        self.connection_label.place(relx=0.98, rely=0.5, anchor="e")
        
        # Main content area
        content_frame = tk.Frame(self.root, bg=COLOR_OCEAN_BG)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Whale widgets
        whale_container = tk.Frame(content_frame, bg=COLOR_OCEAN_BG)
        whale_container.pack(pady=10)
        
        self.whale1 = WhaleWidget(whale_container, "whale_1", self._on_whale_touch)
        self.whale1.pack(side=tk.LEFT, padx=20)
        
        # Connection arrow between whales
        arrow_canvas = tk.Canvas(whale_container, width=80, height=60, 
                                 bg=COLOR_OCEAN_BG, highlightthickness=0)
        arrow_canvas.pack(side=tk.LEFT)
        arrow_canvas.create_text(40, 30, text="⟷", font=("Arial", 32), fill=COLOR_ACCENT)
        
        self.whale2 = WhaleWidget(whale_container, "whale_2", self._on_whale_touch)
        self.whale2.pack(side=tk.LEFT, padx=20)
        
        # Control panel
        self._create_control_panel(content_frame)
        
        # Log panel
        self._create_log_panel(content_frame)
    
    def _create_control_panel(self, parent):
        """Create the control panel."""
        panel_frame = tk.Frame(parent, bg=COLOR_PANEL_BG, pady=10, padx=15)
        panel_frame.pack(fill=tk.X, pady=10)
        
        # Title
        tk.Label(panel_frame, text="Controls", font=("Helvetica", 12, "bold"),
                bg=COLOR_PANEL_BG, fg="white").pack(anchor="w")
        
        controls_row = tk.Frame(panel_frame, bg=COLOR_PANEL_BG)
        controls_row.pack(fill=tk.X, pady=10)
        
        # Color picker button
        self.color_btn = tk.Button(controls_row, text="🎨 Choose Color",
                                   command=self._choose_color,
                                   bg=COLOR_ACCENT, fg="black",
                                   font=("Helvetica", 10, "bold"),
                                   relief=tk.FLAT, padx=15, pady=5)
        self.color_btn.pack(side=tk.LEFT, padx=5)
        
        # Pattern dropdown
        tk.Label(controls_row, text="Pattern:", bg=COLOR_PANEL_BG, fg="white",
                font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(20, 5))
        
        self.pattern_var = tk.StringVar(value="pulse")
        patterns = ["idle", "solid", "pulse", "rainbow", "wave", "sparkle", "breathing"]
        pattern_menu = ttk.Combobox(controls_row, textvariable=self.pattern_var,
                                    values=patterns, state="readonly", width=12)
        pattern_menu.pack(side=tk.LEFT)
        pattern_menu.bind("<<ComboboxSelected>>", self._on_pattern_change)
        
        # Test buttons
        tk.Button(controls_row, text="🐋 Touch Whale 1",
                 command=lambda: self._on_whale_touch("whale_1"),
                 bg="#2D5A7B", fg="white", relief=tk.FLAT,
                 padx=10).pack(side=tk.LEFT, padx=(30, 5))
        
        tk.Button(controls_row, text="🐋 Touch Whale 2",
                 command=lambda: self._on_whale_touch("whale_2"),
                 bg="#2D5A7B", fg="white", relief=tk.FLAT,
                 padx=10).pack(side=tk.LEFT, padx=5)
    
    def _create_log_panel(self, parent):
        """Create the log/message panel."""
        log_frame = tk.Frame(parent, bg=COLOR_PANEL_BG, pady=10, padx=15)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(log_frame, text="Activity Log", font=("Helvetica", 12, "bold"),
                bg=COLOR_PANEL_BG, fg="white").pack(anchor="w")
        
        self.log_text = tk.Text(log_frame, height=6, bg="#0A1A2F", fg="#00FF88",
                               font=("Consolas", 10), relief=tk.FLAT,
                               insertbackground="white")
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self._log("🐋 Pico Whale Simulator started")
        self._log(f"📡 MQTT Topic: {TOPIC_TOUCH}")
    
    def _log(self, message: str):
        """Add message to log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def _connect_mqtt(self):
        """Connect to MQTT broker."""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.connected = True
                client.subscribe(TOPIC_TOUCH)
                client.subscribe(TOPIC_COLOR)
                client.subscribe(TOPIC_PATTERN)
                self.root.after(0, lambda: self._update_connection_status(True))
                self.root.after(0, lambda: self._log("✅ Connected to MQTT broker"))
            else:
                self.root.after(0, lambda: self._log(f"❌ Connection failed: {rc}"))
        
        def on_message(client, userdata, msg):
            topic = msg.topic
            payload = msg.payload.decode()
            self.root.after(0, lambda: self._handle_message(topic, payload))
        
        def on_disconnect(client, userdata, rc):
            self.connected = False
            self.root.after(0, lambda: self._update_connection_status(False))
            self.root.after(0, lambda: self._log("🔌 Disconnected from MQTT"))
        
        try:
            self.mqtt_client = mqtt.Client(client_id=f"simulator_{int(time.time())}")
            self.mqtt_client.on_connect = on_connect
            self.mqtt_client.on_message = on_message
            self.mqtt_client.on_disconnect = on_disconnect
            
            # Connect in background thread
            def connect_thread():
                try:
                    self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
                    self.mqtt_client.loop_start()
                except Exception as e:
                    self.root.after(0, lambda: self._log(f"❌ Connection error: {e}"))
            
            threading.Thread(target=connect_thread, daemon=True).start()
            self._log(f"📡 Connecting to {MQTT_BROKER}...")
            
        except Exception as e:
            self._log(f"❌ MQTT setup error: {e}")
    
    def _update_connection_status(self, connected: bool):
        """Update connection status in UI."""
        if connected:
            self.connection_label.config(text="🟢 Connected", fg=COLOR_CONNECTED)
            self.whale1.set_status(True)
            self.whale2.set_status(True)
        else:
            self.connection_label.config(text="🔴 Disconnected", fg=COLOR_DISCONNECTED)
            self.whale1.set_status(False)
            self.whale2.set_status(False)
    
    def _handle_message(self, topic: str, payload: str):
        """Handle incoming MQTT message."""
        self._log(f"📨 Received: {payload}")
        
        if topic == TOPIC_TOUCH:
            # Parse touch message: "whale_1:touch:timestamp"
            parts = payload.split(":")
            if len(parts) >= 2:
                sender = parts[0]
                # Trigger the OTHER whale to respond
                if sender == "whale_1":
                    self.whale2.start_response()
                    self._log("🐋 Whale 2 responding to Whale 1's touch!")
                elif sender == "whale_2":
                    self.whale1.start_response()
                    self._log("🐋 Whale 1 responding to Whale 2's touch!")
        
        elif topic == TOPIC_COLOR:
            # Parse color message: "r,g,b"
            try:
                r, g, b = map(int, payload.split(","))
                self.whale1.set_color(r, g, b)
                self.whale2.set_color(r, g, b)
                self._log(f"🎨 Color changed to RGB({r},{g},{b})")
            except:
                pass
        
        elif topic == TOPIC_PATTERN:
            self.whale1.set_pattern(payload)
            self.whale2.set_pattern(payload)
            self._log(f"🌊 Pattern changed to: {payload}")
    
    def _on_whale_touch(self, whale_id: str):
        """Handle whale touch event."""
        self._log(f"👆 {whale_id} touched!")
        
        # Send MQTT message
        if self.connected and self.mqtt_client:
            message = f"{whale_id}:touch:{int(time.time())}"
            self.mqtt_client.publish(TOPIC_TOUCH, message)
            self._log(f"📤 Sent: {message}")
        else:
            # Demo mode - trigger response locally
            self._log("📴 Offline mode - simulating local response")
            if whale_id == "whale_1":
                self.whale2.start_response()
            else:
                self.whale1.start_response()
    
    def _choose_color(self):
        """Open color picker dialog."""
        color = colorchooser.askcolor(title="Choose LED Color")
        if color[0]:
            r, g, b = [int(c) for c in color[0]]
            self.whale1.set_color(r, g, b)
            self.whale2.set_color(r, g, b)
            
            # Broadcast color change
            if self.connected and self.mqtt_client:
                self.mqtt_client.publish(TOPIC_COLOR, f"{r},{g},{b}")
            
            self._log(f"🎨 Color set to RGB({r},{g},{b})")
    
    def _on_pattern_change(self, event):
        """Handle pattern selection change."""
        pattern = self.pattern_var.get()
        self.whale1.set_pattern(pattern)
        self.whale2.set_pattern(pattern)
        
        # Broadcast pattern change
        if self.connected and self.mqtt_client:
            self.mqtt_client.publish(TOPIC_PATTERN, pattern)
        
        self._log(f"🌊 Pattern changed to: {pattern}")
    
    def _animation_loop(self):
        """Main animation update loop."""
        self.whale1.update_animation()
        self.whale2.update_animation()
        self.root.after(50, self._animation_loop)  # 20 FPS
    
    def run(self):
        """Start the application."""
        self.root.mainloop()
        
        # Cleanup
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()


# =============================================================================
# Entry Point
# =============================================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  🐋 PICO WHALE DESKTOP SIMULATOR")
    print("=" * 50)
    print(f"  MQTT Broker: {MQTT_BROKER}")
    print(f"  Topic: {TOPIC_TOUCH}")
    print("=" * 50)
    print()
    
    app = PicoWhaleSimulator()
    app.run()
