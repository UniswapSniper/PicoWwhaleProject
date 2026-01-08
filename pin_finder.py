import machine
import time

print("\n" + "="*40)
print("🔍 PIN FINDER TOOL")
print("="*40)
print("Please TAP the sensor continuously for 10 seconds!")
print("Checking GPIOs: 11, 12, 13, 14, 15, 16, 17")

# Pin 15 = Expected (Physical 20)
# Pin 11 = Physical Pin 15 (Common Mistake)
# Pin 14 = Sound Sensor
candidates = [15, 11, 14, 16, 17, 12, 13]
pins = {}

for p in candidates:
    try:
        # Use Pull Down so disconnected/floating wires usually read 0
        pins[p] = machine.Pin(p, machine.Pin.IN, machine.Pin.PULL_DOWN)
    except:
        pass

# Scan loop
for i in range(100):
    detected = []
    for p, pin in pins.items():
        if pin.value() == 1:
            detected.append(str(p))
    
    if detected:
        print(f"  👉 ACTIVE: GPIO {', '.join(detected)}")
    
    time.sleep(0.1)

print("Scan complete.\n")
