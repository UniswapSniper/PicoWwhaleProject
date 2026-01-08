#!/bin/bash
# 🐋 Quick test to verify Pico is connected and working

MPREMOTE="/Users/jeffgoldner/Library/Python/3.9/bin/mpremote"

echo "🐋 Pico Whale Connection Test"
echo "=============================="
echo ""

# Check if mpremote is available
if [ ! -f "$MPREMOTE" ]; then
    echo "❌ mpremote not installed"
    echo "Run: pip3 install mpremote"
    exit 1
fi

echo "✅ mpremote is installed"
echo ""

# Test connection
echo "📡 Scanning for Pico W..."
$MPREMOTE connect list
echo ""

# Try to get version
echo "🔍 Checking MicroPython version..."
$MPREMOTE exec "import sys; print(sys.version)"
echo ""

# List files
echo "📁 Files on Pico:"
$MPREMOTE exec "import os; [print(f'  - {f}') for f in os.listdir('/')]"
echo ""

# Check if main files exist
echo "🔍 Checking required files..."
$MPREMOTE exec "
import os
files = os.listdir('/')
required = ['main.py', 'config.py']
for f in required:
    if f in files:
        print(f'  ✅ {f}')
    else:
        print(f'  ❌ {f} (MISSING)')
        
if 'animations.py' in files:
    print('  ✅ animations.py (optional)')
else:
    print('  ⚠️  animations.py (recommended)')
"
echo ""
echo "=============================="
echo "Test complete!"
echo ""
echo "To deploy files: ./deploy_to_pico.sh"
echo "To access REPL:  ./pico_repl.sh"
echo ""
