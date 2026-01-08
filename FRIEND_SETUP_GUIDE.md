# 🐋 Moving Your Whale to a Friend's House

**The Mystery Solved:** Your home router (`Inseego FX3100`) uses **5G Cellular Internet**. Cellular networks operate differently from standard home internet—they have strict firewalls that block the specific "language" (MQTT) our whales use to talk.

**The Solution:** Moving the whale to a friend's house with standard **Cable or Fiber internet** (like Comcast, AT&T, or Verizon Fios) will remove this block instantly!

---

## 📋 The 3-Step Information Checklist

### 1. 📝 Get Credentials
Ask your friend for their exact:
- **WiFi Name (SSID)**
- **WiFi Password**

### 2. ⚙️ Update Code
Open `src/config.py` on your computer and update just these lines:

```python
# CHANGE THESE FOR FRIEND'S WIFI:
WIFI_SSID = "Friends_WiFi_Name"
WIFI_PASSWORD = "Friends_Password"

# IF THIS IS THE SECOND WHALE (Friend's Whale):
DEVICE_ID = "whale_2" 
```

### 3. 🚀 Deploy
Plug the Pico into your computer and run:
`./deploy_to_pico.sh`

---

## ✅ How to Know It Worked
Run the monitor:
`./pico_repl.sh`

**At your friend's house:**
`✅ WiFi connected!`
`✅ MQTT connected!`

**At your house:**
`⚠ MQTT failed - running in offline demo mode` (This is normal behavior for your network!)
