# Query 4: Docker USB Configuration for Windows 11 (2025-2026)

**Status:** RESEARCH COMPLETE
**Date:** January 12, 2026
**Source:** Official Microsoft WSL Documentation + Stack Overflow Best Practices
**Retrieved:** From Microsoft Learn, Docker Forums, and 2025 production deployments

---

## 1. Architecture: How USB Works with Docker on Windows 11

### The Challenge

Docker on Windows 11 runs in **WSL2 (Windows Subsystem for Linux 2)**, which is a lightweight Linux VM. USB devices attached to Windows are NOT automatically visible to Linux containers.

### Solution: USB/IP Protocol

Microsoft provides **usbipd-win** (USB/IP for Windows) which:
1. Shares USB devices from Windows to WSL2
2. Makes them appear as `/dev/ttyUSB0` or `/dev/ttyACM0` in Linux
3. Works seamlessly with Docker containers running in WSL2

### Three-Layer Architecture

```
Windows 11 (Host)
  └─ USB Device (COM3)
      └─ USBIPD-WIN (usbipd-win tool)
          └─ WSL2 Distribution (Ubuntu, Debian)
              └─ Docker Engine
                  └─ Container (Your Flask App)
                      └─ /dev/ttyUSB0 (appears here)
```

---

## 2. Windows 11 Prerequisites and Setup

### System Requirements

- **Windows 11** (Build 22000 or later)
  - Windows 10 is not supported for USB passthrough
  - Verify version: `winver` in PowerShell

- **WSL2 Enabled**
  ```powershell
  # Check current WSL version
  wsl -l -v

  # Should show:
  # NAME                   STATE           VERSION
  # Ubuntu-22.04           Running         2  <-- Must be 2
  ```

- **Virtualization Enabled in BIOS**
  - Check: Settings → System → About → Device specifications
  - Look for: "Virtualization: Enabled"

- **Docker Desktop** (Latest)
  - Settings → General → ✓ Use the WSL 2 based engine
  - Settings → Resources → WSL Integration → ✓ Ubuntu (or your distro)

### Installation Steps

**Step 1: Install usbipd-win**

```powershell
# Option A: Using WinGet (Recommended for Windows 11)
winget install dorssel.usbipd-win

# Option B: Manual download
# Go to: https://github.com/dorssel/usbipd-win/releases
# Download and install MSI file

# Verify installation
usbipd --version
```

**Step 2: Verify WSL2 Linux Distribution**

```powershell
# List attached devices (should already show your arm)
lsusb   # Run inside WSL2 (wsl lsusb)

# OR from Windows, list USB devices
usbipd list
# Example output:
# BUSID  VID:PID             DEVICE                                STATE
# 1-1    2341:0043           Arduino Micro (COM3)                  Not shared
# 3-5    2c9f:2000           USB2.0-Serial (SwiftArm Pro)          Not shared
```

**Step 3: Enable Required Kernel Modules (Critical!)**

```bash
# Run inside WSL2 Ubuntu terminal
sudo modprobe vhci-hcd
sudo modprobe usbip-core

# Make permanent by editing /etc/modules
sudo nano /etc/modules
# Add these lines:
# vhci-hcd
# usbip-core

# Save: Ctrl+O, Enter, Ctrl+X
```

---

## 3. USB Device Binding and Attachment Process

### Understanding Binding vs Attachment

| Operation | Scope | Persistence | Purpose |
|-----------|-------|-------------|---------|
| **Bind** | Windows only | Persistent (until unbound) | Share device to USB/IP |
| **Attach** | WSL2 | Session-based | Connect bound device to specific WSL distro |

### Step-by-Step Process

**Step 1: List Available USB Devices (Windows PowerShell)**

```powershell
# Open PowerShell as Administrator
# Right-click PowerShell → Run as Administrator

usbipd list

# Example output:
# BUSID  VID:PID             DEVICE                    STATE
# 1-1    2c9f:2000           USB2.0-Serial (SwiftArm)  Not shared
# 3-5    1a86:7523           CH340 Serial              Not shared
```

**Step 2: Bind USB Device (Windows PowerShell - Admin)**

```powershell
# Replace BUSID with your device
# For SwiftArm: usually 1-1 or similar

usbipd bind --busid 1-1

# Verify binding
usbipd list
# Should show STATE as "Shared"
```

**Step 3: Attach to WSL2 (Windows PowerShell)**

```powershell
# Attach to WSL2
usbipd attach --wsl --busid 1-1

# Verify attachment in PowerShell
usbipd list
# Should show STATE as "Attached"
```

**Step 4: Verify in WSL2 Linux**

```bash
# Inside WSL2 (Ubuntu terminal)

# Check USB devices visible in Linux
lsusb

# Example output:
# Bus 002 Device 002: ID 2c9f:2000 USB2.0-Serial

# Check serial ports
ls -la /dev/tty*

# Should show: /dev/ttyUSB0 or /dev/ttyACM0
```

### Complete Example: SwiftArm Pro USB Attachment

```powershell
# PowerShell (Admin)

# 1. List devices
usbipd list

# 2. Identify SwiftArm (typically shows as "USB2.0-Serial" or similar)
# 3. Bind it
usbipd bind --busid 1-1

# 4. Attach to WSL2
usbipd attach --wsl --busid 1-1

# 5. Verify
usbipd list   # Should show "Attached"
```

```bash
# WSL2 Terminal

# 6. Confirm Linux sees it
lsusb
ls -la /dev/ttyUSB0

# 7. Test communication (optional)
echo "test" > /dev/ttyUSB0
```

---

## 4. Docker Compose Configuration

### Basic docker-compose.yml with USB Device

```yaml
# docker-compose.yml
version: '3.9'

services:
  swift_arm_controller:
    build: .
    container_name: swift_arm_flask

    # Map serial port into container
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0

    # Ports for Flask API
    ports:
      - "5000:5000"  # Flask server

    # Environment variables
    environment:
      - FLASK_ENV=production
      - ARM_PORT=/dev/ttyUSB0
      - ARM_BAUDRATE=115200

    # Restart policy
    restart: unless-stopped

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

### Production-Grade Configuration

```yaml
version: '3.9'

services:
  swift_arm_api:
    build:
      context: .
      dockerfile: Dockerfile

    container_name: swift_arm_controller

    # USB Device Mapping
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0
      - /dev/bus/usb:/dev/bus/usb  # Alternative: raw USB access

    # Port Bindings
    ports:
      - "5000:5000"
      - "5001:5001"  # Backup port

    # Volumes for Logging
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config:ro

    # Environment
    environment:
      FLASK_ENV: production
      LOG_LEVEL: INFO
      ARM_SERIAL_PORT: /dev/ttyUSB0
      ARM_BAUDRATE: 115200
      ARM_TIMEOUT: 5
      WORKERS: 4

    # Health Check (important!)
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

    # Restart Strategy
    restart: on-failure:5

    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

    # Resource Limits
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M

    # Networking
    networks:
      - arm_network

networks:
  arm_network:
    driver: bridge
```

### Key Configuration Explanations

| Setting | Value | Why |
|---------|-------|-----|
| `devices: /dev/ttyUSB0:/dev/ttyUSB0` | Serial device mapping | Maps host USB to container |
| `ports: 5000:5000` | Flask API port | Accessible from Windows host |
| `healthcheck` | 30s interval | Detects if Flask crashes |
| `restart: on-failure:5` | Auto-restart limit | Prevents infinite restart loop |
| `cpus: 2.0` | Max 2 cores | Limits resource usage |
| `memory: 1G` | Max 1GB RAM | Prevents runaway processes |

---

## 5. Dockerfile for SwiftArm Flask Backend

### Minimal Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY main.py .

# Create logs directory
RUN mkdir -p /app/logs

# Run Flask app
CMD ["python", "main.py"]
```

### Production Dockerfile with Non-Root User

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     curl     && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser main.py .

# Create directories
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3     CMD curl -f http://localhost:5000/api/status || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "30", "main:app"]
```

---

## 6. Common Windows 11 + WSL2 + Docker Issues and Fixes

### Issue 1: Device Not Visible in Linux (/dev/ttyUSB0 Missing)

**Symptoms:**
```bash
# Inside container
ls /dev/tty*
# Shows nothing or only tty0, console, etc.
```

**Solutions:**

```bash
# A. Check kernel modules are loaded
sudo modprobe vhci-hcd
sudo modprobe usbip-core

# B. Reload modules
sudo modprobe -r vhci-hcd
sudo modprobe vhci-hcd

# C. Check usbipd status from Windows
usbipd list  # Should show "Attached"

# D. Restart WSL2
wsl --terminate Ubuntu  # From PowerShell
wsl  # Restart
```

### Issue 2: "Permission Denied" on /dev/ttyUSB0

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '/dev/ttyUSB0'
```

**Solutions:**

```bash
# Option A: Add user to dialout group (inside WSL)
sudo usermod -a -G dialout $USER
# Logout and login again
exit
# Re-enter WSL

# Option B: Change device permissions (temporary, resets on reboot)
sudo chmod 666 /dev/ttyUSB0

# Option C: Using docker-compose, set --privileged (less secure)
privileged: true  # In docker-compose.yml
```

### Issue 3: Device Disconnects or Becomes "Not Shared"

**Symptoms:**
```
usbipd list
# Shows: Not shared or Attached then suddenly Not shared
```

**Solutions:**

```powershell
# A. Manual re-bind and re-attach
usbipd bind --busid 1-1
usbipd attach --wsl --busid 1-1

# B. Restart Docker and containers
docker-compose down
docker-compose up -d

# C. Restart WSL (nuclear option)
wsl --shutdown
docker-compose up -d
```

### Issue 4: "vhci_hcd module loading failed"

**Symptoms:**
```
usbipd: error: Loading vhci_hcd failed
```

**Solutions:**

```bash
# Inside WSL Ubuntu terminal
sudo modprobe vhci-hcd
sudo modprobe usbip-core

# If fails, update WSL kernel
wsl --update  # From PowerShell (Admin)

# Make modules load at boot
echo "vhci-hcd" | sudo tee -a /etc/modules
echo "usbip-core" | sudo tee -a /etc/modules
sudo reboot
```

### Issue 5: "Device Already in Use by Host"

**Symptoms:**
```
usbipd: error: Cannot attach device, device may already be in use by the host
```

**Solutions:**

```powershell
# A. Unbind first
usbipd unbind --busid 1-1

# B. Stop any Windows programs using serial port
# Check Device Manager: COM3 or similar
# Close any terminal emulator or IDE using COM3

# C. Re-bind and attach
usbipd bind --busid 1-1
usbipd attach --wsl --busid 1-1
```

---

## 7. Testing USB Access in Docker Container

### Quick Test Script

```python
# test_usb.py - Run inside container to verify USB access
import serial
import sys

def test_usb_access():
    port = '/dev/ttyUSB0'

    try:
        # Test 1: File exists
        import os
        if not os.path.exists(port):
            print(f"❌ Port {port} does not exist")
            print("Available devices:", os.listdir('/dev/tty*'))
            return False

        print(f"✓ Port {port} exists")

        # Test 2: Can open
        ser = serial.Serial(port, 115200, timeout=1)
        print(f"✓ Successfully opened {port} at 115200 baud")

        # Test 3: Send command
        ser.write(b'#1 P2220
')
        response = ser.readline()
        print(f"✓ Sent command, received: {response}")

        ser.close()
        print("✓ ALL TESTS PASSED")
        return True

    except PermissionError:
        print(f"❌ Permission denied on {port}")
        print("   Try: sudo usermod -a -G dialout $USER")
        return False

    except FileNotFoundError:
        print(f"❌ {port} not found")
        print("   Check: usbipd list (should show 'Attached')")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_usb_access()
    sys.exit(0 if success else 1)
```

### Run Test in Container

```bash
# Build and run test
docker build -t swift-arm-test .
docker run --rm --device=/dev/ttyUSB0:/dev/ttyUSB0 swift-arm-test python test_usb.py

# Expected output:
# ✓ Port /dev/ttyUSB0 exists
# ✓ Successfully opened /dev/ttyUSB0 at 115200 baud
# ✓ Sent command, received: b'$1 ok X...
# ✓ ALL TESTS PASSED
```

---

## 8. Production Deployment Checklist

### Pre-Deployment Windows 11

- [ ] Windows 11 Build 22000+ installed (`winver`)
- [ ] WSL2 enabled and updated (`wsl --update`)
- [ ] Docker Desktop installed with WSL2 backend
- [ ] usbipd-win installed (`usbipd --version`)
- [ ] Virtualization enabled in BIOS
- [ ] USB kernel modules available (`lsmod | grep usb`)

### Pre-Deployment WSL2/Linux

- [ ] USB kernel modules loaded:
  ```bash
  sudo modprobe vhci-hcd
  sudo modprobe usbip-core
  ```
- [ ] Modules persist across reboot (in `/etc/modules`)
- [ ] User can access USB: `sudo usermod -a -G dialout $USER`
- [ ] SwiftArm device visible: `lsusb | grep 2c9f:2000`

### Before Running Docker Container

- [ ] USB device bound: `usbipd bind --busid X-X`
- [ ] USB device attached: `usbipd attach --wsl --busid X-X`
- [ ] Verified in Linux: `ls -la /dev/ttyUSB0`
- [ ] docker-compose.yml has `devices: /dev/ttyUSB0:/dev/ttyUSB0`
- [ ] Port 5000 not in use: `netstat -ano | findstr :5000`

### Container Running

- [ ] Can run container: `docker-compose up`
- [ ] Container shows healthy: `docker ps` → STATUS: Up
- [ ] API responds: `curl http://localhost:5000/api/status`
- [ ] Logs show no errors: `docker-compose logs`

### Testing USB Communication

- [ ] Position query works: 
  ```
  curl http://localhost:5000/api/status
  # Response: {"status": "connected", "position": {...}}
  ```
- [ ] Movement works: 
  ```
  curl -X POST http://localhost:5000/api/move -H "Content-Type: application/json" -d '{"x":100, "y":0, "z":50, "speed":1000}'
  ```
- [ ] Emergency stop works: 
  ```
  curl -X POST http://localhost:5000/api/emergency-stop
  ```

---

## Summary: Windows 11 Docker USB Setup

✓ Install **usbipd-win** on Windows  
✓ Enable **kernel modules** in WSL2 (vhci-hcd, usbip-core)  
✓ **Bind** USB device in Windows (admin PowerShell)  
✓ **Attach** USB device to WSL2 (PowerShell)  
✓ Map device in **docker-compose.yml** (`devices: /dev/ttyUSB0`)  
✓ Test with **Python serial test** inside container  
✓ Run Flask app with USB access working  

---

**Document:** Query 4 - Docker USB Configuration for Windows 11 (COMPLETE)
**Status:** Ready for container deployment
**Last Updated:** January 12, 2026
**Source:** Official Microsoft WSL Documentation + Production Patterns 2025
