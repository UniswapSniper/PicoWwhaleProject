# 🐋 Pico Whale - Command Line Deployment Guide

## No VS Code Required! 🎉

You can do everything from the terminal using `mpremote`.

---

## Quick Start

### 1. Test Connection

```bash
./test_pico_connection.sh
```

This checks if your Pico is connected and shows what files are on it.

### 2. Deploy Everything

```bash
./deploy_to_pico.sh
```

This automatically:
- Uploads all files to your Pico
- Connects to WiFi
- Installs umqtt library
- Reboots the Pico to start your app

### 3. Access REPL (if needed)

```bash
./pico_repl.sh
```

This gives you direct access to the Pico's Python prompt.
Press `Ctrl+X` to exit.

---

## Individual Commands

### Check Pico Connection
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote connect list
```

### Upload a Single File
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote cp src/main.py :main.py
```

### Run Code on Pico
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote exec "print('Hello from Pico!')"
```

### List Files on Pico
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote exec "import os; print(os.listdir('/'))"
```

### Soft Reset (Restart)
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote exec "import machine; machine.soft_reset()"
```

### Access REPL Directly
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote repl
```

---

## Troubleshooting

### "command not found: mpremote"

The scripts handle this automatically. If you want to use `mpremote` directly, either:

**Option A: Use full path:**
```bash
/Users/jeffgoldner/Library/Python/3.9/bin/mpremote --help
```

**Option B: Add to PATH:**
```bash
export PATH="/Users/jeffgoldner/Library/Python/3.9/bin:$PATH"
```

### "No MicroPython device found"

1. Make sure Pico W is plugged in via USB
2. Check if another program is using the serial port
3. Unplug and replug the USB cable

### "Permission denied" on scripts

```bash
chmod +x *.sh
```

---

## Recommended Workflow

**First Time Setup:**
1. `./test_pico_connection.sh` - Verify Pico is connected
2. Edit `src/config.py` with your WiFi credentials
3. `./deploy_to_pico.sh` - Deploy everything

**After Deployment:**
- `./pico_repl.sh` - Watch the output, see touch events
- Touch your sensor and watch the terminal!

**Making Changes:**
1. Edit files in `src/` folder
2. `./deploy_to_pico.sh` - Re-deploy
3. `./pico_repl.sh` - Watch it run

---

## All Available Scripts

| Script | Purpose |
|--------|---------|
| `test_pico_connection.sh` | Check if Pico is connected |
| `deploy_to_pico.sh` | Full deployment (all files + setup) |
| `pico_repl.sh` | Access Python prompt on Pico |

**No VS Code needed!** 🎉
