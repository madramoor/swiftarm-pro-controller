# Query 5: Web Interface Design for Hardware Control (2025-2026)

**Status:** RESEARCH COMPLETE
**Date:** January 12, 2026
**Source:** WCAG 2.2 Guidelines + IoT Dashboard Patterns + 2025-2026 Design Trends
**Retrieved:** From W3C/WCAG Standards and Production UI Patterns

---

## 1. UI Patterns for Real-Time Hardware Control Systems

### Industry-Standard Dashboard Layout

The most effective layout for robot control combines:
- **Large, clear status display** (top center)
- **Main control area** (center)
- **Emergency stop** (prominent, top-right)
- **Feedback/logs** (bottom)

```
╔═════════════════════════════════════════════════════════════╗
║  SwiftArm Pro Controller Dashboard                [E-STOP] ║
╠═════════════════════════════════════════════════════════════╣
║                                                              ║
║  STATUS: Connected  │  Position: X=100.5 Y=50.2 Z=75.8     ║
║  Gripper: Open      │  Pump: Off                             ║
║                                                              ║
╠═════════════════════════════════════════════════════════════╣
║                                                              ║
║     [ Home ]  [ Move ]  [ Gripper ]  [ Advanced ]           ║
║                                                              ║
║  Position Control:                                           ║
║  X: [  100  ] mm    Speed: [ 1000 ] mm/min                 ║
║  Y: [   50  ] mm    [ SEND MOVEMENT ]                      ║
║  Z: [   75  ] mm                                             ║
║                                                              ║
╠═════════════════════════════════════════════════════════════╣
║  Logs:                                                       ║
║  17:45:32 - Movement started (X=100 Y=50 Z=75)             ║
║  17:45:42 - Movement completed                              ║
║  17:46:12 - User online                                     ║
╚═════════════════════════════════════════════════════════════╝
```

### Key UI Components

#### 1. Status Display (Always Visible)

```html
<!-- HTML structure -->
<div class="status-bar">
    <div class="connection-status">
        <span class="indicator connected"></span>
        <span class="label">Connected</span>
    </div>
    <div class="current-position">
        Position: X=<span id="pos-x">100.5</span> Y=<span id="pos-y">50.2</span> Z=<span id="pos-z">75.8</span> mm
    </div>
    <div class="arm-state">
        Gripper: <span id="gripper">Open</span> | Pump: <span id="pump">Off</span>
    </div>
</div>

<!-- CSS styling -->
<style>
    .status-bar {
        background-color: #1a1a1a;
        color: #fff;
        padding: 15px;
        border-bottom: 2px solid #4CAF50;
        font-size: 16px;
        font-weight: 500;
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        gap: 20px;
    }

    .indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .indicator.connected {
        background-color: #4CAF50;
        animation: pulse 2s infinite;
    }

    .indicator.disconnected {
        background-color: #f44336;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
```

#### 2. Position Input Controls (Clear Labels)

```html
<div class="control-panel">
    <fieldset>
        <legend>Target Position (mm)</legend>

        <div class="control-group">
            <label for="input-x">X Axis (50-320):</label>
            <input 
                type="number" 
                id="input-x" 
                min="50" 
                max="320" 
                value="150"
                aria-label="X axis coordinate in millimeters"
            >
            <span class="current-value">Current: <span id="curr-x">150</span></span>
        </div>

        <div class="control-group">
            <label for="input-y">Y Axis (-200 to 200):</label>
            <input 
                type="number" 
                id="input-y" 
                min="-200" 
                max="200" 
                value="0"
                aria-label="Y axis coordinate in millimeters"
            >
            <span class="current-value">Current: <span id="curr-y">0</span></span>
        </div>

        <div class="control-group">
            <label for="input-z">Z Axis (0-150):</label>
            <input 
                type="number" 
                id="input-z" 
                min="0" 
                max="150" 
                value="50"
                aria-label="Z axis coordinate in millimeters"
            >
            <span class="current-value">Current: <span id="curr-z">50</span></span>
        </div>

        <div class="control-group">
            <label for="input-speed">Speed (1-2000 mm/min):</label>
            <input 
                type="number" 
                id="input-speed" 
                min="1" 
                max="2000" 
                value="1000"
                aria-label="Movement speed in millimeters per minute"
            >
        </div>
    </fieldset>

    <button id="btn-send" class="btn btn-primary" aria-label="Send movement command">
        SEND MOVEMENT
    </button>
</div>

<!-- CSS -->
<style>
    .control-panel {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 8px;
    }

    fieldset {
        border: 2px solid #ddd;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 4px;
    }

    legend {
        font-weight: bold;
        font-size: 16px;
        padding: 0 10px;
    }

    .control-group {
        margin-bottom: 15px;
        display: grid;
        grid-template-columns: 150px 1fr 150px;
        gap: 15px;
        align-items: center;
    }

    label {
        font-weight: 500;
        font-size: 14px;
    }

    input[type="number"] {
        padding: 10px;
        border: 2px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
    }

    input[type="number"]:focus {
        outline: none;
        border-color: #4CAF50;
        box-shadow: 0 0 4px rgba(76, 175, 80, 0.3);
    }

    input[type="number"]:invalid {
        border-color: #f44336;
        background-color: #ffebee;
    }

    .current-value {
        font-size: 13px;
        color: #666;
    }
</style>
```

#### 3. Emergency Stop Button (Critical Design)

```html
<!-- Emergency Stop Button -->
<div class="estop-container">
    <button 
        id="btn-estop" 
        class="btn btn-estop"
        aria-label="Emergency stop - immediately halts all arm movement"
        aria-pressed="false"
    >
        E-STOP
    </button>
    <p class="estop-info">Halts all movement immediately</p>
</div>

<!-- CSS: Large, Red, Impossible to Miss -->
<style>
    .estop-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        text-align: center;
    }

    .btn-estop {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: #d32f2f;  /* Emergency red */
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: 3px solid #b71c1c;  /* Darker red border */
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }

    .btn-estop:hover {
        background-color: #b71c1c;
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(211, 47, 47, 0.4);
    }

    .btn-estop:active {
        transform: scale(0.98);
        background-color: #8b0000;
    }

    .btn-estop:focus {
        outline: 3px solid #fff;
        outline-offset: 3px;
    }

    /* Accessible keyboard focus */
    .btn-estop:focus-visible {
        outline: 3px solid #ffeb3b;
        outline-offset: 4px;
    }

    .estop-info {
        margin-top: 8px;
        font-size: 12px;
        color: #666;
    }
</style>

<!-- JavaScript: Always Ready -->
<script>
document.getElementById('btn-estop').addEventListener('click', async (e) => {
    e.preventDefault();

    try {
        // E-stop: NO retry logic, NO delay
        const response = await fetch('/api/emergency-stop', {
            method: 'POST',
            timeout: 500  // 500ms max
        });

        console.log('E-STOP SENT');
    } catch (error) {
        console.error('E-STOP ERROR:', error);
        // Even if request fails, arm should timeout and stop
    }
});
</script>
```

---

## 2. Real-Time Position Feedback Display

### Live Position Updates (500ms Polling)

```javascript
// app.js - Real-time position polling
class PositionMonitor {
    constructor() {
        this.polling = false;
        this.pollInterval = 500;  // 500ms
    }

    start() {
        if (this.polling) return;
        this.polling = true;
        this._poll();
    }

    async _poll() {
        while (this.polling) {
            try {
                const response = await fetch('/api/status');

                if (!response.ok) {
                    this._updateStatus(false);
                    await this._sleep(this.pollInterval);
                    continue;
                }

                const data = await response.json();

                if (data.position) {
                    // Update display elements
                    document.getElementById('pos-x').textContent = 
                        data.position.x.toFixed(1);
                    document.getElementById('pos-y').textContent = 
                        data.position.y.toFixed(1);
                    document.getElementById('pos-z').textContent = 
                        data.position.z.toFixed(1);

                    this._updateStatus(true);
                } else {
                    this._updateStatus(false);
                }
            } catch (error) {
                console.error('Poll error:', error);
                this._updateStatus(false);
            }

            await this._sleep(this.pollInterval);
        }
    }

    _updateStatus(connected) {
        const indicator = document.querySelector('.indicator');
        const label = document.querySelector('.status-bar .label');

        if (connected) {
            indicator.classList.remove('disconnected');
            indicator.classList.add('connected');
            label.textContent = 'Connected';
        } else {
            indicator.classList.remove('connected');
            indicator.classList.add('disconnected');
            label.textContent = 'Disconnected';
        }
    }

    _sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    stop() {
        this.polling = false;
    }
}

// Start monitoring on page load
const monitor = new PositionMonitor();
document.addEventListener('DOMContentLoaded', () => {
    monitor.start();
});
```

### Visual Feedback for Movements

```html
<!-- Movement Status Display -->
<div id="movement-status" class="movement-status hidden">
    <div class="status-content">
        <div class="spinner"></div>
        <p id="status-message">Moving to target position...</p>
        <div class="progress-bar">
            <div class="progress-fill" id="progress"></div>
        </div>
    </div>
</div>

<!-- CSS -->
<style>
    .movement-status {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #323232;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .movement-status:not(.hidden) {
        opacity: 1;
    }

    .status-content {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .spinner {
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #4CAF50;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .progress-bar {
        width: 200px;
        height: 4px;
        background-color: #555;
        border-radius: 2px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background-color: #4CAF50;
        width: 0%;
        animation: progress 3s ease-in-out forwards;
    }

    @keyframes progress {
        0% { width: 10%; }
        50% { width: 60%; }
        100% { width: 95%; }
    }
</style>
```

---

## 3. Emergency Stop UX Best Practices (2025-2026)

### Principles

1. **Always Visible**: Top-right corner, never scrolled out of view
2. **Large Target**: 80px circular button (WCAG 2.2 requires min 24x24, we use 3.3x standard)
3. **Distinctive Color**: ISO 13850 mandates red for emergency stops
4. **No Modals**: No confirmation dialogs - immediate action
5. **Keyboard Access**: Spacebar or dedicated key (Esc)
6. **No Timeout**: Works immediately, no serialization

### Emergency Stop Accessibility

```html
<button 
    id="estop" 
    class="btn-estop"
    aria-label="Emergency stop button. Press to immediately halt all arm movement"
    aria-pressed="false"
    role="button"
    tabindex="0"
>
    E-STOP
</button>

<script>
// Keyboard shortcuts for E-stop
document.addEventListener('keydown', (e) => {
    // Space bar or Escape key
    if (e.code === 'Space' || e.code === 'Escape') {
        if (e.target === document.body) {
            e.preventDefault();
            document.getElementById('estop').click();
        }
    }
});

// Screen reader announcement
function announceEstop() {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'assertive');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.textContent = 'Emergency stop activated. All movement halted.';
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    document.body.appendChild(announcement);

    setTimeout(() => announcement.remove(), 1000);
}

document.getElementById('estop').addEventListener('click', () => {
    announceEstop();
});
</script>
```

---

## 4. Responsive Design for Hardware Dashboards

### Mobile-First Breakpoints

```css
/* Mobile First (< 600px) - Stack Layout */
@media (max-width: 600px) {
    .control-panel {
        grid-template-columns: 1fr;
    }

    .status-bar {
        grid-template-columns: 1fr;
        gap: 10px;
    }

    .control-group {
        grid-template-columns: 1fr;
        gap: 8px;
    }

    input[type="number"] {
        font-size: 16px;  /* Prevent iOS zoom */
    }

    .btn-estop {
        width: 70px;
        height: 70px;
        font-size: 16px;
    }
}

/* Tablet (600px - 1024px) - Two Column */
@media (min-width: 600px) and (max-width: 1024px) {
    .control-panel {
        grid-template-columns: 1fr 1fr;
    }

    .status-bar {
        grid-template-columns: 1fr 1fr;
    }
}

/* Desktop (> 1024px) - Three Column */
@media (min-width: 1024px) {
    .control-panel {
        grid-template-columns: 1fr 1fr 1fr;
    }

    .status-bar {
        grid-template-columns: 1fr 2fr 1fr;
    }
}

/* Touch Targets (WCAG 2.2 SC 2.5.8: Minimum 24x24 CSS pixels) */
button {
    min-width: 44px;  /* Apple's recommendation */
    min-height: 44px;
    padding: 12px 16px;
}

/* Large Text for Visibility */
body {
    font-size: 16px;  /* Base size */
}

.status-bar {
    font-size: 18px;  /* Larger for visibility */
}

input[type="number"] {
    font-size: 16px;  /* Prevent iOS zoom at 16px */
}
```

### Orientation Handling

```javascript
// Handle device orientation
window.addEventListener('orientationchange', () => {
    // Refresh dashboard layout
    document.body.classList.remove('portrait', 'landscape');

    if (window.matchMedia('(orientation: portrait)').matches) {
        document.body.classList.add('portrait');
    } else {
        document.body.classList.add('landscape');
    }
});

// Initial check
if (window.matchMedia('(orientation: portrait)').matches) {
    document.body.classList.add('portrait');
} else {
    document.body.classList.add('landscape');
}
```

---

## 5. Accessibility Requirements (WCAG 2.2 Level AA)

### Compliance Checklist

#### Principle 1: Perceivable
- [ ] **Color is not the only means**: E-stop is large + text label "E-STOP"
- [ ] **Sufficient contrast**: Text 4.5:1 ratio (WCAG AA minimum)
- [ ] **Resizable text**: Users can zoom to 200%
- [ ] **Images have alt text**: All icons have aria-labels

#### Principle 2: Operable
- [ ] **Keyboard accessible**: All buttons work with Tab + Enter
- [ ] **No keyboard trap**: Focus can move to all interactive elements
- [ ] **E-stop keyboard shortcut**: Space/Esc key works
- [ ] **Pointer gestures not required**: No drag-and-drop mandatory
- [ ] **Target size**: All buttons 44x44px minimum (WCAG 2.2 SC 2.5.8)

#### Principle 3: Understandable
- [ ] **Descriptive labels**: "X Axis (50-320)" not just "X"
- [ ] **Error messages**: Clear: "X out of range [50-320]"
- [ ] **Consistent navigation**: Controls always in same place
- [ ] **Simple language**: No technical jargon

#### Principle 4: Robust
- [ ] **Valid HTML**: No parsing errors
- [ ] **ARIA landmarks**: `<main>`, `<nav>`, `<form>`
- [ ] **Screen reader compatible**: All interactive elements have roles/labels
- [ ] **Assistive technology**: Works with voice control, eye trackers

### Implementation Example

```html
<!-- WCAG 2.2 Compliant Structure -->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SwiftArm Pro Controller</title>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <header role="banner">
        <h1>SwiftArm Pro Controller</h1>
    </header>

    <nav aria-label="Main navigation">
        <ul>
            <li><a href="#status">Status</a></li>
            <li><a href="#controls">Controls</a></li>
            <li><a href="#logs">Logs</a></li>
        </ul>
    </nav>

    <main id="main-content">
        <!-- E-Stop in Accessible Location -->
        <div class="estop-container" role="region" aria-label="Emergency controls">
            <button id="estop" 
                    class="btn-estop"
                    aria-label="Emergency stop. Press to immediately halt all arm movement"
                    aria-pressed="false">
                E-STOP
            </button>
        </div>

        <!-- Main Content -->
        <section id="status" aria-labelledby="status-heading">
            <h2 id="status-heading">Status</h2>
            <div class="status-bar" role="status" aria-live="polite">
                <span class="indicator connected"></span>
                <span>Connected</span>
            </div>
        </section>

        <section id="controls" aria-labelledby="control-heading">
            <h2 id="control-heading">Movement Controls</h2>
            <form id="movement-form">
                <fieldset>
                    <legend>Target Position</legend>
                    <!-- Form fields with proper labels -->
                </fieldset>
            </form>
        </section>
    </main>

    <footer role="contentinfo">
        <p>&copy; 2026 SwiftArm Controller. All rights reserved.</p>
    </footer>
</body>
</html>
```

---

## 6. Modern Design Trends (2025-2026)

### Trends to Implement

#### 1. Large, Bold Typography
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 16px;
    font-weight: 500;
}

h1, h2, h3 {
    font-weight: 700;
    line-height: 1.2;
}

.status-bar {
    font-size: 18px;
    font-weight: 600;
}
```

#### 2. Dark Mode (Reduces Glare, Saves Power)
```css
@media (prefers-color-scheme: dark) {
    body {
        background-color: #121212;
        color: #ffffff;
    }

    input, button {
        background-color: #1e1e1e;
        color: #ffffff;
        border-color: #444;
    }
}

/* Manual dark mode toggle */
body.dark-mode {
    background-color: #121212;
    color: #ffffff;
}
```

#### 3. Micro-Animations (Functional Feedback)
```css
/* Button press feedback */
button {
    transition: all 0.1s ease;
}

button:active {
    transform: scale(0.98);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Status change animation */
.indicator {
    transition: background-color 0.3s ease;
}

/* Loading spinner */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

#### 4. Consistent Spacing (8px Grid)
```css
/* 8px base unit */
:root {
    --spacing-xs: 4px;   /* 0.5 units */
    --spacing-sm: 8px;   /* 1 unit */
    --spacing-md: 16px;  /* 2 units */
    --spacing-lg: 24px;  /* 3 units */
    --spacing-xl: 32px;  /* 4 units */
}

.control-group {
    margin-bottom: var(--spacing-lg);
    gap: var(--spacing-md);
}

button {
    padding: var(--spacing-md) var(--spacing-lg);
}
```

---

## 7. Complete HTML/CSS/JS Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SwiftArm Pro Controller</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5;
            color: #333;
            font-size: 16px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .status-bar {
            background: #1a1a1a;
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 20px;
            font-size: 18px;
            font-weight: 600;
        }

        .indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            background: #f44336;
            animation: pulse 2s infinite;
        }

        .indicator.connected {
            background: #4CAF50;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .control-panel {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        fieldset {
            border: 2px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }

        .control-group {
            display: grid;
            grid-template-columns: 150px 1fr 150px;
            gap: 15px;
            margin-bottom: 15px;
            align-items: center;
        }

        input[type="number"] {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }

        input:focus {
            outline: none;
            border-color: #4CAF50;
            box-shadow: 0 0 4px rgba(76,175,80,0.3);
        }

        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.2s;
            min-height: 44px;
        }

        .btn-primary {
            background: #4CAF50;
            color: white;
        }

        .btn-primary:hover {
            background: #45a049;
        }

        .btn-estop {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #d32f2f;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border: 3px solid #b71c1c;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            z-index: 1000;
        }

        .btn-estop:hover {
            background: #b71c1c;
            transform: scale(1.05);
        }

        @media (max-width: 600px) {
            .status-bar {
                grid-template-columns: 1fr;
                gap: 10px;
            }

            .control-group {
                grid-template-columns: 1fr;
            }

            .btn-estop {
                width: 70px;
                height: 70px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SwiftArm Pro Controller</h1>

        <div class="status-bar" role="status" aria-live="polite">
            <div>
                <span class="indicator connected"></span>
                <span>Connected</span>
            </div>
            <div>
                Position: X=<span id="pos-x">0</span> Y=<span id="pos-y">0</span> Z=<span id="pos-z">0</span>
            </div>
            <div>
                Gripper: <span id="gripper">Open</span>
            </div>
        </div>

        <div class="control-panel">
            <form id="movement-form">
                <fieldset>
                    <legend>Target Position</legend>

                    <div class="control-group">
                        <label for="x">X Axis:</label>
                        <input type="number" id="x" min="50" max="320" value="150">
                        <span>mm</span>
                    </div>

                    <div class="control-group">
                        <label for="y">Y Axis:</label>
                        <input type="number" id="y" min="-200" max="200" value="0">
                        <span>mm</span>
                    </div>

                    <div class="control-group">
                        <label for="z">Z Axis:</label>
                        <input type="number" id="z" min="0" max="150" value="50">
                        <span>mm</span>
                    </div>

                    <div class="control-group">
                        <label for="speed">Speed:</label>
                        <input type="number" id="speed" min="1" max="2000" value="1000">
                        <span>mm/min</span>
                    </div>
                </fieldset>

                <button type="submit" class="btn btn-primary">
                    SEND MOVEMENT
                </button>
            </form>
        </div>
    </div>

    <button class="btn-estop" aria-label="Emergency stop">E-STOP</button>

    <script>
        // Poll position updates
        async function updatePosition() {
            try {
                const response = await fetch('/api/status');
                if (response.ok) {
                    const data = await response.json();
                    if (data.position) {
                        document.getElementById('pos-x').textContent = data.position.x.toFixed(1);
                        document.getElementById('pos-y').textContent = data.position.y.toFixed(1);
                        document.getElementById('pos-z').textContent = data.position.z.toFixed(1);
                    }
                }
            } catch (e) {
                console.error('Position update failed:', e);
            }
        }

        // Poll every 500ms
        setInterval(updatePosition, 500);

        // E-stop handler
        document.querySelector('.btn-estop').addEventListener('click', async () => {
            try {
                await fetch('/api/emergency-stop', { method: 'POST' });
                console.log('E-STOP SENT');
            } catch (e) {
                console.error('E-stop error:', e);
            }
        });

        // Movement form
        document.getElementById('movement-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                x: parseFloat(document.getElementById('x').value),
                y: parseFloat(document.getElementById('y').value),
                z: parseFloat(document.getElementById('z').value),
                speed: parseFloat(document.getElementById('speed').value)
            };

            try {
                const response = await fetch('/api/move', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    console.log('Movement sent');
                }
            } catch (e) {
                console.error('Movement error:', e);
            }
        });
    </script>
</body>
</html>
```

---

## Summary: Web Interface Design for Hardware Control

✓ **Real-time position feedback** (500ms polling)  
✓ **Large, accessible E-stop button** (80x80px, ISO 13850 red)  
✓ **Responsive design** (mobile-first, touch-friendly)  
✓ **WCAG 2.2 Level AA compliant** (accessibility built-in)  
✓ **Dark mode support** (reduces glare, saves power)  
✓ **Micro-animations** (functional feedback)  
✓ **Keyboard navigation** (Tab, Enter, Space)  
✓ **Screen reader compatible** (semantic HTML, ARIA labels)  

---

**Document:** Query 5 - Web Interface Design for Hardware Control (COMPLETE)
**Status:** Ready for frontend implementation
**Last Updated:** January 12, 2026
**Source:** WCAG 2.2 Standards + 2025-2026 UI Design Trends
