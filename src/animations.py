# Pico Whale Project - Animation Library
# ========================================
# Reusable LED animation patterns for NeoPixel rings/strips
# Works with MicroPython on Raspberry Pi Pico W

import time
import math

try:
    import random
except ImportError:
    # MicroPython fallback
    from urandom import getrandbits
    class RandomFallback:
        @staticmethod
        def random():
            return getrandbits(16) / 65535
        @staticmethod
        def randint(a, b):
            return a + (getrandbits(16) % (b - a + 1))
    random = RandomFallback()


class AnimationLibrary:
    """
    LED animation patterns for NeoPixel rings/strips.
    
    Usage:
        from animations import AnimationLibrary
        
        anim = AnimationLibrary(led_count=12)
        anim.set_color(255, 100, 200)  # Pink
        
        while True:
            colors = anim.pulse()
            for i, color in enumerate(colors):
                np[i] = color
            np.write()
            time.sleep(0.05)
    """
    
    def __init__(self, led_count: int = 12):
        """Initialize animation library.
        
        Args:
            led_count: Number of LEDs in the strip/ring
        """
        self.led_count = led_count
        self.red = 255
        self.green = 100
        self.blue = 200
        self._tick = 0
        self._offset = 0.0
        
    def set_color(self, r: int, g: int, b: int):
        """Set the base color for animations.
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        self.red = max(0, min(255, r))
        self.green = max(0, min(255, g))
        self.blue = max(0, min(255, b))
    
    def _clamp(self, value: int) -> int:
        """Clamp value to valid LED range."""
        return max(0, min(255, int(value)))
    
    # =========================================================================
    # Animation Patterns
    # =========================================================================
    
    def off(self) -> list:
        """All LEDs off."""
        return [(0, 0, 0)] * self.led_count
    
    def solid(self, brightness: float = 1.0) -> list:
        """Solid color at specified brightness.
        
        Args:
            brightness: Brightness level (0.0 - 1.0)
        """
        r = self._clamp(self.red * brightness)
        g = self._clamp(self.green * brightness)
        b = self._clamp(self.blue * brightness)
        return [(r, g, b)] * self.led_count
    
    def idle(self) -> list:
        """Dim blue idle state - indicates whale is connected but waiting."""
        return [(10, 30, 60)] * self.led_count
    
    def pulse(self, speed: float = 3.0) -> list:
        """Pulsing brightness animation.
        
        Args:
            speed: Pulse speed multiplier
        """
        self._tick += 1
        t = self._tick * 0.05 * speed
        brightness = 0.3 + 0.7 * abs(math.sin(t))
        return self.solid(brightness)
    
    def breathing(self, speed: float = 0.5) -> list:
        """Slow breathing glow effect - very smooth and calming.
        
        Args:
            speed: Breathing speed multiplier
        """
        self._tick += 1
        t = self._tick * 0.05 * speed
        # Natural breathing curve
        brightness = (math.exp(math.sin(t)) - 0.36787944) / 2.35040238
        return self.solid(brightness)
    
    def rainbow(self, speed: float = 1.0) -> list:
        """Rainbow cycle around the LED ring.
        
        Args:
            speed: Rotation speed multiplier
        """
        colors = []
        self._offset = (self._offset + 0.01 * speed) % 1.0
        
        for i in range(self.led_count):
            hue = (i / self.led_count + self._offset) % 1.0
            r, g, b = self._hsv_to_rgb(hue, 1.0, 1.0)
            colors.append((self._clamp(r * 255), 
                          self._clamp(g * 255), 
                          self._clamp(b * 255)))
        return colors
    
    def wave(self, speed: float = 3.0) -> list:
        """Wave pattern traveling around the ring.
        
        Args:
            speed: Wave speed multiplier
        """
        colors = []
        self._tick += 1
        t = self._tick * 0.05 * speed
        
        for i in range(self.led_count):
            offset = (i / self.led_count * 2 * math.pi) + t
            brightness = 0.2 + 0.8 * (math.sin(offset) + 1) / 2
            r = self._clamp(self.red * brightness)
            g = self._clamp(self.green * brightness)
            b = self._clamp(self.blue * brightness)
            colors.append((r, g, b))
        return colors
    
    def sparkle(self, density: float = 0.15) -> list:
        """Random sparkle effect with white flashes.
        
        Args:
            density: Probability of sparkle per LED (0.0 - 1.0)
        """
        colors = []
        for _ in range(self.led_count):
            if random.random() < density:
                colors.append((255, 255, 255))
            else:
                r = self._clamp(self.red * 0.3)
                g = self._clamp(self.green * 0.3)
                b = self._clamp(self.blue * 0.3)
                colors.append((r, g, b))
        return colors
    
    def comet(self, tail_length: int = 4, speed: float = 1.0) -> list:
        """Comet/shooting star effect traveling around ring.
        
        Args:
            tail_length: Length of the comet tail
            speed: Movement speed
        """
        colors = [(0, 0, 0)] * self.led_count
        self._tick += 1
        
        # Calculate comet head position
        position = int((self._tick * 0.2 * speed) % self.led_count)
        
        for i in range(tail_length):
            led_pos = (position - i) % self.led_count
            brightness = 1.0 - (i / tail_length)
            r = self._clamp(self.red * brightness)
            g = self._clamp(self.green * brightness)
            b = self._clamp(self.blue * brightness)
            colors[led_pos] = (r, g, b)
        
        return colors
    
    def alternate(self, speed: float = 2.0) -> list:
        """Alternating LEDs blink pattern.
        
        Args:
            speed: Blink speed
        """
        self._tick += 1
        phase = int(self._tick * 0.1 * speed) % 2
        
        colors = []
        for i in range(self.led_count):
            if (i % 2) == phase:
                colors.append((self.red, self.green, self.blue))
            else:
                r = self._clamp(self.red * 0.1)
                g = self._clamp(self.green * 0.1)
                b = self._clamp(self.blue * 0.1)
                colors.append((r, g, b))
        return colors
    
    def fire(self) -> list:
        """Flickering fire/candle effect."""
        colors = []
        for _ in range(self.led_count):
            # Random flicker
            flicker = 0.7 + random.random() * 0.3
            # Fire colors (orange-yellow-red)
            r = self._clamp(255 * flicker)
            g = self._clamp((50 + random.randint(0, 100)) * flicker)
            b = 0
            colors.append((r, g, b))
        return colors
    
    def ocean(self, speed: float = 1.0) -> list:
        """Gentle ocean wave in blues and teals.
        
        Args:
            speed: Wave speed
        """
        colors = []
        self._tick += 1
        t = self._tick * 0.03 * speed
        
        for i in range(self.led_count):
            offset = (i / self.led_count * 2 * math.pi) + t
            wave1 = (math.sin(offset) + 1) / 2
            wave2 = (math.sin(offset * 1.5 + 1.2) + 1) / 2
            brightness = 0.3 + 0.7 * (wave1 * 0.6 + wave2 * 0.4)
            
            # Ocean colors
            r = self._clamp(20 * brightness)
            g = self._clamp((100 + 50 * wave2) * brightness)
            b = self._clamp((180 + 75 * wave1) * brightness)
            colors.append((r, g, b))
        return colors
    
    def flash(self, on_frames: int = 5, off_frames: int = 5) -> list:
        """Simple on/off flash pattern.
        
        Args:
            on_frames: Number of frames LED stays on
            off_frames: Number of frames LED stays off
        """
        self._tick += 1
        cycle_length = on_frames + off_frames
        
        if (self._tick % cycle_length) < on_frames:
            return self.solid()
        else:
            return self.off()
    
    def celebration(self) -> list:
        """Colorful celebration pattern - random colors and sparkles."""
        colors = []
        for _ in range(self.led_count):
            if random.random() < 0.3:
                # Random bright color
                hue = random.random()
                r, g, b = self._hsv_to_rgb(hue, 1.0, 1.0)
                colors.append((self._clamp(r * 255), 
                              self._clamp(g * 255), 
                              self._clamp(b * 255)))
            else:
                colors.append((0, 0, 0))
        return colors
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> tuple:
        """Convert HSV to RGB color space.
        
        Args:
            h: Hue (0.0 - 1.0)
            s: Saturation (0.0 - 1.0)
            v: Value/brightness (0.0 - 1.0)
            
        Returns:
            Tuple of (r, g, b) as floats (0.0 - 1.0)
        """
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
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)
    
    def reset(self):
        """Reset animation state."""
        self._tick = 0
        self._offset = 0.0


# =============================================================================
# Convenience Functions
# =============================================================================

def get_pattern_names() -> list:
    """Get list of available pattern names."""
    return [
        "off", "solid", "idle", "pulse", "breathing", 
        "rainbow", "wave", "sparkle", "comet", "alternate",
        "fire", "ocean", "flash", "celebration"
    ]


def run_pattern(anim: AnimationLibrary, pattern_name: str) -> list:
    """Run a pattern by name.
    
    Args:
        anim: AnimationLibrary instance
        pattern_name: Name of the pattern to run
        
    Returns:
        List of RGB tuples for each LED
    """
    patterns = {
        "off": anim.off,
        "solid": anim.solid,
        "idle": anim.idle,
        "pulse": anim.pulse,
        "breathing": anim.breathing,
        "rainbow": anim.rainbow,
        "wave": anim.wave,
        "sparkle": anim.sparkle,
        "comet": anim.comet,
        "alternate": anim.alternate,
        "fire": anim.fire,
        "ocean": anim.ocean,
        "flash": anim.flash,
        "celebration": anim.celebration,
    }
    
    func = patterns.get(pattern_name, anim.idle)
    return func()


# =============================================================================
# Demo Mode
# =============================================================================

if __name__ == "__main__":
    # Demo: Print pattern colors to console
    print("🐋 Animation Library Demo")
    print("=" * 40)
    
    anim = AnimationLibrary(led_count=12)
    anim.set_color(255, 100, 200)
    
    for pattern in get_pattern_names():
        colors = run_pattern(anim, pattern)
        print(f"\n{pattern}:")
        for i, c in enumerate(colors):
            print(f"  LED {i:2d}: RGB{c}")
        anim.reset()
