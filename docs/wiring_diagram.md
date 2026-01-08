# 🔌 Wiring Diagram

## Pico W Pinout Reference

```
                    ┌─────────────────────┐
              GP0  ─┤ 1               40 ├─ VBUS (5V from USB)
              GP1  ─┤ 2               39 ├─ VSYS (System voltage)
             GND   ─┤ 3               38 ├─ GND
              GP2  ─┤ 4               37 ├─ 3V3_EN
              GP3  ─┤ 5               36 ├─ 3V3 (3.3V output) ★
              GP4  ─┤ 6               35 ├─ ADC_VREF
              GP5  ─┤ 7               34 ├─ GP28
             GND   ─┤ 8               33 ├─ GND ★
              GP6  ─┤ 9               32 ├─ GP27
              GP7  ─┤ 10              31 ├─ GP26
              GP8  ─┤ 11              30 ├─ RUN
              GP9  ─┤ 12              29 ├─ GP22
             GND   ─┤ 13              28 ├─ GND
             GP10  ─┤ 14              27 ├─ GP21
             GP11  ─┤ 15              26 ├─ GP20
             GP12  ─┤ 16              25 ├─ GP19
             GP13  ─┤ 17              24 ├─ GP18
             GND   ─┤ 18              23 ├─ GND
             GP14  ─┤ 19              22 ├─ GP17 ★ (Vibration Motor)
             GP15  ─┤ 20 ★ (Touch)   21 ├─ GP16 ★ (NeoPixel)
                    └─────────────────────┘
```

## Component Wiring

### 1. Capacitive Touch Sensor (TTP223)

The TTP223 is a simple capacitive touch sensor module.

```
TTP223          Pico W
┌─────┐
│ VCC ├────────► 3V3 (Pin 36)
│ GND ├────────► GND (Pin 33 or any GND)
│ SIG ├────────► GP15 (Pin 20)
└─────┘
```

**Notes:**
- The touch area can be extended with a wire or conductive tape
- Some modules have a configuration jumper - set to "toggle" or "momentary" mode

### 2. NeoPixel LED Ring (WS2812B)

```
NeoPixel        Pico W
┌─────┐
│ VCC ├────────► VBUS (Pin 40) or external 5V
│ GND ├────────► GND (Pin 33 or any GND)
│ DIN ├────────► GP16 (Pin 21)
└─────┘
```

**Important:**
- NeoPixels can draw significant current - use external power for many LEDs
- Add a 300-500Ω resistor between GP16 and DIN for signal protection
- A 1000µF capacitor across power can prevent issues

### 3. Micro Servo (9g) - Tail Flapping
The Servo is used to give the whale physical movement.

```
Servo           Pico W
┌─────┐
│ Red ├─────────► VBUS (Pin 40 - 5V)
│ Black ├──────► GND (Pin 38)
│ Orange├──────► GP17 (Pin 22)
└─────┘
```

**Note:** If moving a larger part, consider an external 5V power supply to avoid drawing too much from the Pico.

### 4. Sound Sensor (Microphone)
Allows the whale to respond to claps or speech.

```
Sound Sensor    Pico W
┌─────┐
│ VCC ├────────► 3V3 (Pin 36)
│ GND ├────────► GND (Pin 33)
│ DO  ├────────► GP14 (Pin 19)
└─────┘
```

**Tip:** Use the small potentiometer on the sensor to adjust sensitivity.

## Complete Breadboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│                      BREADBOARD                              │
│                                                              │
│  [NeoPixel Ring]                                             │
│       │                                                      │
│       │ (DIN)                                                │
│       │                                                      │
│  ┌────┴─────────────────────────────────────────────────┐   │
│  │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●   │   │
│  │    1    2    3    4    5    6    7    8    9    10  │   │
│  │                                                      │   │
│  │  ┌─────────────────────┐                            │   │
│  │  │                     │                            │   │
│  │  │     PICO W          │      [Touch Sensor]        │   │
│  │  │                     │           │                │   │
│  │  │     (USB port)      │           │ (SIG)          │   │
│  │  │         ▲           │           │                │   │
│  │  └─────────────────────┘           │                │   │
│  │                                                      │   │
│  │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  + Power Rail (Red) ────────────────────────────── +        │
│  - Ground Rail (Blue) ──────────────────────────── -        │
└─────────────────────────────────────────────────────────────┘
```

## Shopping List

| Component | Example Product | Approx Cost |
|-----------|----------------|-------------|
| Raspberry Pi Pico W | Official Pico W | $6-8 |
| TTP223 Touch Sensor | Amazon/AliExpress | $1-3 |
| WS2812B Ring (12 LED) | NeoPixel Ring | $5-10 |
| Vibration Motor | Small coin motor | $1-2 |
| Breadboard | Half-size breadboard | $3-5 |
| Jumper Wires | Assorted pack | $3-5 |
| USB Cable | Micro USB | $2-3 |
| **Total per whale** | | **~$25-35** |

## Tips

1. **Test each component individually** before combining
2. **Double-check power connections** - wrong voltage can damage parts
3. **Use different colored wires** for power (red), ground (black), and signals
4. **Keep wires short** to reduce noise and improve reliability
