/**
 * 🐋 Pico Whale Control Panel - JavaScript Application
 * =====================================================
 * Handles MQTT communication and UI interactions
 */

// =============================================================================
// Configuration
// =============================================================================

const CONFIG = {
    mqtt: {
        broker: 'wss://test.mosquitto.org:8081', // WebSocket secure
        wsBroker: 'ws://test.mosquitto.org:8080', // WebSocket (fallback)
        pairId: 'whale_pair_jeff_friend',
        topics: {
            touch: null,      // Set dynamically
            heartbeat: null,
            color: null,
            pattern: null,
            status: null
        }
    },
    animation: {
        responseTime: 5000,  // How long whale responds (ms)
        ledCount: 12
    }
};

// Set topics dynamically
CONFIG.mqtt.topics.touch = `pico_whale/${CONFIG.mqtt.pairId}/touch`;
CONFIG.mqtt.topics.heartbeat = `pico_whale/${CONFIG.mqtt.pairId}/heartbeat`;
CONFIG.mqtt.topics.color = `pico_whale/${CONFIG.mqtt.pairId}/color`;
CONFIG.mqtt.topics.pattern = `pico_whale/${CONFIG.mqtt.pairId}/pattern`;
CONFIG.mqtt.topics.status = `pico_whale/${CONFIG.mqtt.pairId}/status`;

// =============================================================================
// State
// =============================================================================

const state = {
    connected: false,
    mqttClient: null,
    currentColor: { r: 255, g: 100, b: 200 },
    currentPattern: 'pulse',
    whale1Responding: false,
    whale2Responding: false,
    animationFrame: null
};

// =============================================================================
// DOM Elements
// =============================================================================

const elements = {
    connectionStatus: null,
    statusDot: null,
    statusText: null,
    logContainer: null,
    colorPicker: null,
    whale1Ring: null,
    whale2Ring: null,
    whale1Card: null,
    whale2Card: null,
    patternButtons: null,
    colorPresets: null
};

// =============================================================================
// Initialize
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initElements();
    initEventListeners();
    startLEDAnimation();
    connectMQTT();
    log('🐋 Pico Whale Control Panel initialized', 'info');
});

function initElements() {
    elements.connectionStatus = document.getElementById('connectionStatus');
    elements.statusDot = elements.connectionStatus?.querySelector('.status-dot');
    elements.statusText = elements.connectionStatus?.querySelector('.status-text');
    elements.logContainer = document.getElementById('logContainer');
    elements.colorPicker = document.getElementById('colorPicker');
    elements.whale1Ring = document.getElementById('whale1Ring');
    elements.whale2Ring = document.getElementById('whale2Ring');
    elements.whale1Card = document.getElementById('whale1Card');
    elements.whale2Card = document.getElementById('whale2Card');
    elements.patternButtons = document.querySelectorAll('.pattern-btn');
    elements.colorPresets = document.querySelectorAll('.color-preset');
}

function initEventListeners() {
    // Color picker
    if (elements.colorPicker) {
        elements.colorPicker.addEventListener('input', (e) => {
            const color = hexToRgb(e.target.value);
            if (color) {
                state.currentColor = color;
                sendColor(color);
            }
        });
    }

    // Color presets
    elements.colorPresets.forEach(btn => {
        btn.addEventListener('click', () => {
            const colorHex = btn.dataset.color;
            const color = hexToRgb(colorHex);
            if (color) {
                state.currentColor = color;
                elements.colorPicker.value = colorHex;

                // Update active state
                elements.colorPresets.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                sendColor(color);
            }
        });
    });

    // Pattern buttons
    elements.patternButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const pattern = btn.dataset.pattern;
            state.currentPattern = pattern;

            // Update active state
            elements.patternButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            sendPattern(pattern);
        });
    });
}

// =============================================================================
// MQTT Connection
// =============================================================================

function connectMQTT() {
    updateConnectionStatus('connecting');
    log(`📡 Connecting to MQTT broker...`, 'info');

    try {
        // Try secure WebSocket first
        const clientId = `web_control_${Date.now()}`;

        state.mqttClient = mqtt.connect(CONFIG.mqtt.broker, {
            clientId: clientId,
            clean: true,
            connectTimeout: 10000,
            reconnectPeriod: 5000
        });

        state.mqttClient.on('connect', () => {
            state.connected = true;
            updateConnectionStatus('connected');
            log('✅ Connected to MQTT broker', 'success');

            // Subscribe to all topics
            const topics = Object.values(CONFIG.mqtt.topics);
            state.mqttClient.subscribe(topics, (err) => {
                if (err) {
                    log(`❌ Subscribe error: ${err.message}`, 'error');
                } else {
                    log(`📬 Subscribed to whale topics`, 'info');
                }
            });
        });

        state.mqttClient.on('message', (topic, message) => {
            handleMQTTMessage(topic, message.toString());
        });

        state.mqttClient.on('error', (err) => {
            log(`❌ MQTT error: ${err.message}`, 'error');
            updateConnectionStatus('disconnected');
        });

        state.mqttClient.on('close', () => {
            state.connected = false;
            updateConnectionStatus('disconnected');
            log('🔌 Connection closed', 'warning');
        });

        state.mqttClient.on('reconnect', () => {
            log('🔄 Reconnecting...', 'info');
            updateConnectionStatus('connecting');
        });

    } catch (err) {
        log(`❌ Connection error: ${err.message}`, 'error');
        updateConnectionStatus('disconnected');
    }
}

function handleMQTTMessage(topic, payload) {
    const topicName = topic.split('/').pop();
    log(`📨 [${topicName}] ${payload}`, 'info');

    if (topic === CONFIG.mqtt.topics.touch) {
        // Parse touch message: "whale_1:touch:timestamp"
        const parts = payload.split(':');
        if (parts.length >= 2) {
            const sender = parts[0];
            // Trigger the OTHER whale to respond
            if (sender === 'whale_1') {
                startWhaleResponse('whale_2');
            } else if (sender === 'whale_2') {
                startWhaleResponse('whale_1');
            }
        }
    } else if (topic === CONFIG.mqtt.topics.color) {
        // Parse color: "r,g,b"
        try {
            const [r, g, b] = payload.split(',').map(Number);
            state.currentColor = { r, g, b };
            elements.colorPicker.value = rgbToHex(r, g, b);
        } catch (e) { }
    } else if (topic === CONFIG.mqtt.topics.pattern) {
        state.currentPattern = payload;
        elements.patternButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.pattern === payload);
        });
    }
}

function updateConnectionStatus(status) {
    if (!elements.statusDot || !elements.statusText) return;

    elements.statusDot.classList.remove('connected', 'disconnected', 'connecting');

    switch (status) {
        case 'connected':
            elements.statusDot.classList.add('connected');
            elements.statusText.textContent = 'Connected';
            break;
        case 'disconnected':
            elements.statusDot.classList.add('disconnected');
            elements.statusText.textContent = 'Disconnected';
            break;
        case 'connecting':
            elements.statusDot.classList.add('connecting');
            elements.statusText.textContent = 'Connecting...';
            break;
    }
}

// =============================================================================
// MQTT Publish Functions
// =============================================================================

function sendTouch(whaleId) {
    const message = `${whaleId}:touch:${Date.now()}`;

    if (state.connected && state.mqttClient) {
        state.mqttClient.publish(CONFIG.mqtt.topics.touch, message);
        log(`📤 Sent touch from ${whaleId}`, 'success');
    } else {
        // Demo mode
        log(`📴 Offline - simulating ${whaleId} touch`, 'warning');
        const otherWhale = whaleId === 'whale_1' ? 'whale_2' : 'whale_1';
        startWhaleResponse(otherWhale);
    }
}

function sendColor(color) {
    const message = `${color.r},${color.g},${color.b}`;

    if (state.connected && state.mqttClient) {
        state.mqttClient.publish(CONFIG.mqtt.topics.color, message);
        log(`🎨 Color set to RGB(${color.r}, ${color.g}, ${color.b})`, 'info');
    } else {
        log(`🎨 Color set locally (offline)`, 'warning');
    }
}

function sendPattern(pattern) {
    if (state.connected && state.mqttClient) {
        state.mqttClient.publish(CONFIG.mqtt.topics.pattern, pattern);
        log(`🌊 Pattern set to: ${pattern}`, 'info');
    } else {
        log(`🌊 Pattern set locally (offline)`, 'warning');
    }
}

// =============================================================================
// Whale Response Animation
// =============================================================================

function startWhaleResponse(whaleId) {
    const isWhale1 = whaleId === 'whale_1';
    const card = isWhale1 ? elements.whale1Card : elements.whale2Card;

    if (isWhale1) {
        state.whale1Responding = true;
    } else {
        state.whale2Responding = true;
    }

    // Add responding class
    card?.classList.add('responding');
    log(`🐋 ${whaleId.replace('_', ' ')} is responding!`, 'success');

    // End response after duration
    setTimeout(() => {
        if (isWhale1) {
            state.whale1Responding = false;
        } else {
            state.whale2Responding = false;
        }
        card?.classList.remove('responding');
    }, CONFIG.animation.responseTime);
}

// =============================================================================
// LED Animation Loop
// =============================================================================

function startLEDAnimation() {
    function animate() {
        updateLEDs(elements.whale1Ring, state.whale1Responding);
        updateLEDs(elements.whale2Ring, state.whale2Responding);
        state.animationFrame = requestAnimationFrame(animate);
    }
    animate();
}

function updateLEDs(ringElement, isResponding) {
    if (!ringElement) return;

    const leds = ringElement.querySelectorAll('.led');
    const now = Date.now();

    leds.forEach((led, index) => {
        if (isResponding) {
            // Pulse effect when responding
            const phase = (now / 300) % 2;
            led.classList.toggle('active', phase < 1);

            // Set color
            const brightness = 0.5 + 0.5 * Math.sin(now / 300);
            const r = Math.floor(state.currentColor.r * brightness);
            const g = Math.floor(state.currentColor.g * brightness);
            const b = Math.floor(state.currentColor.b * brightness);
            led.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
            led.style.boxShadow = `0 0 10px rgb(${r}, ${g}, ${b})`;
        } else {
            // Idle state - dim blue
            led.classList.remove('active');
            led.style.backgroundColor = '#112233';
            led.style.boxShadow = 'none';
        }
    });
}

// =============================================================================
// Quick Actions
// =============================================================================

function syncAll() {
    log('🔄 Syncing all whales...', 'info');
    sendColor(state.currentColor);
    sendPattern(state.currentPattern);
    log('✅ Sync complete', 'success');
}

function turnOff() {
    state.currentPattern = 'off';
    if (state.connected && state.mqttClient) {
        state.mqttClient.publish(CONFIG.mqtt.topics.pattern, 'off');
    }
    log('🌙 Whales turned off', 'info');

    elements.patternButtons.forEach(btn => {
        btn.classList.remove('active');
    });
}

function testConnection() {
    if (state.connected) {
        log('📡 Connection test: MQTT connected!', 'success');
        // Send a heartbeat
        const msg = JSON.stringify({
            device: 'web_panel',
            status: 'online',
            timestamp: Date.now()
        });
        state.mqttClient.publish(CONFIG.mqtt.topics.heartbeat, msg);
    } else {
        log('📡 Connection test: Not connected to MQTT', 'error');
    }
}

// =============================================================================
// Logging
// =============================================================================

function log(message, type = 'info') {
    const container = elements.logContainer;
    if (!container) return;

    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;

    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { hour12: false });

    entry.innerHTML = `
        <span class="log-time">${time}</span>
        <span class="log-message">${message}</span>
    `;

    container.appendChild(entry);
    container.scrollTop = container.scrollHeight;

    // Limit log entries
    while (container.children.length > 50) {
        container.removeChild(container.firstChild);
    }
}

// =============================================================================
// Utility Functions
// =============================================================================

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(x => {
        const hex = Math.round(x).toString(16);
        return hex.length === 1 ? '0' + hex : hex;
    }).join('');
}

// =============================================================================
// Expose Global Functions (for inline onclick handlers)
// =============================================================================

window.sendTouch = sendTouch;
window.syncAll = syncAll;
window.turnOff = turnOff;
window.testConnection = testConnection;
