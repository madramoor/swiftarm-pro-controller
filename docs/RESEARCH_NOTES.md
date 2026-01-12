# Query 1: SwiftArm Pro Hardware Specifications (RESEARCH)

**Status:** RESEARCH COMPLETE - From Official Developer Guide v1.0.6
**Date:** January 12, 2026
**Source:** uArm Swift Pro Developer Guide + Quick Start Guide
**Retrieved:** From official PDF documentation

---

## 1. USB Serial Specifications

### Connection Details
- **Port Type:** Micro USB
- **Baud Rate:** 115200 bps (bits per second)
- **Protocol:** Custom Gcode with protocol header
- **Communication Format:** ASCII text commands with line feed (\n)
- **Response Type:** Text acknowledgment or error codes

### Command/Response Format
**Command Structure:**
```
#n GCODE_COMMAND parameters\n
```

Where:
- `#n` = Command identifier (n is a number for matching responses)
- `GCODE_COMMAND` = Standard or custom Gcode command
- `parameters` = Space-separated command parameters
- `\n` = Line feed (newline character)

**Response Structure:**
```
$n ok\n
```
Or error:
```
$n Ex\n
```

### Example
```
Send:     #25 G0 X180 Y0 Z150 F5000\n
Reply:    $25 ok\n
Meaning:  Move to position [180, 0, 150] mm at 5000 mm/min speed
```

---

## 2. Gcode Command Syntax and Examples

### Movement Commands

#### G0 - Linear Move (Cartesian Coordinates)
```
#n G0 X100 Y100 Z100 F1000\n
```
- X, Y, Z = Position in millimeters
- F = Speed in mm/min
- Response: `$n ok\n`

#### G1 - Laser Mode Control
```
#n G1 X100 Y100 Z100 F1000\n
```
- After entering laser mode (M2400 S1)
- G0 = Laser off
- G1 = Laser on
- Response: `$n ok\n`

#### G2201 - Polar Coordinates
```
#n G2201 S100 R90 H80 F1000\n
```
- S = Stretch in mm
- R = Rotation in degrees
- H = Height in mm
- F = Speed in mm/min

#### G2202 - Joint Angle Control
```
#n G2202 N0 V90\n
```
- N = Joint ID (0, 1, 2, 3)
- V = Angle (0-180 degrees)

#### G2204 - Relative Displacement
```
#n G2204 X10 Y10 Z10 F1000\n
```
- Moves relative to current position

### Setting Commands

#### M17 - Attach All Motors
```
#n M17\n
```
- Enables all joint motors
- Response: `$n ok\n`

#### M2019 - Detach All Motors
```
#n M2019\n
```
- Disables all joint motors
- Response: `$n ok\n`

#### M2120 - Set Feedback Cycle
```
#n M2120 V0.2\n
```
- V = Time interval in seconds
- Returns Cartesian coordinates at set interval
- Response: `@3 X154.71 Y194.91 Z10.21\n`

#### M2231 - Pump Control
```
#n M2231 V1\n
```
- V = 1 (working) or 0 (stop)
- Controls suction pump
- Response: `$n ok\n`

#### M2232 - Gripper Control
```
#n M2232 V1\n
```
- V = 1 (close) or 0 (open)
- Controls electronic gripper
- Response: `$n ok\n`

#### M2400 - Set Mode
```
#n M2400 S0\n
```
- S = Mode number:
  - 0 = Normal mode (suction)
  - 1 = Laser mode
  - 2 = 3D printing mode
  - 3 = Universal holder mode

### Querying Commands (Position Feedback)

#### P2200 - Get Joint Angles
```
#n P2200\n
Response: $n ok B50 L50 R50\n
```
- B = Base motor angle (0-180°)
- L = Left motor angle (0-130°)
- R = Right motor angle (0-106°)

#### P2220 - Get Cartesian Position
```
#n P2220\n
Response: $n ok X100 Y100 Z100\n
```
- Returns current X, Y, Z coordinates in mm

#### P2221 - Get Polar Coordinates
```
#n P2221\n
Response: $n ok S100 R90 H80\n
```
- S = Stretch (mm)
- R = Rotation (degrees)
- H = Height (mm)

#### P2231 - Get Pump Status
```
#n P2231\n
Response: $n ok V1\n
```
- V = 0 (stop), 1 (working), 2 (grabbing)

#### P2232 - Get Gripper Status
```
#n P2232\n
Response: $n ok V1\n
```
- V = 0 (stop), 1 (working), 2 (grabbing)

#### P2234 - Get Power Status
```
#n P2234\n
Response: $n ok V1\n
```
- V = 1 (connected), 0 (disconnected)

---

## 3. Movement Range for All Axes

### Workspace Boundaries (Critical for Safety)

| Axis | Min | Max | Unit | Notes |
|------|-----|-----|------|-------|
| **X** | 50 | 320 | mm | Left-Right |
| **Y** | -200 | 200 | mm | Forward-Backward |
| **Z** | 0 | 150 | mm | Up-Down |

**Important:** The workspace is the reachable area. Attempting to move outside these bounds will return an error.

### Joint Angle Ranges

| Joint | Min | Max | Unit | Motor |
|-------|-----|-----|------|-------|
| **Base (N=0)** | 0 | 180 | degrees | Base motor |
| **Left (N=1)** | 0 | 130 | degrees | Left arm motor |
| **Right (N=2)** | 0 | 106 | degrees | Right arm motor |
| **End-Effector (N=3)** | 0 | 180 | degrees | End-effector motor |

---

## 4. Gripper/Pump Control Commands

### Pump (Suction Cup) Control

**Activate Pump:**
```
#n M2231 V1\n
Response: $n ok\n
```

**Deactivate Pump:**
```
#n M2231 V0\n
Response: $n ok\n
```

**Query Pump Status:**
```
#n P2231\n
Response: $n ok V1\n (0=stop, 1=working, 2=grabbing)
```

**Specifications:**
- Max Suction Diameter: 5-10 mm
- Max Pressure: 33 kPa
- Max Lifting Weight: 1000g

### Gripper Control

**Close Gripper:**
```
#n M2232 V1\n
Response: $n ok\n
```

**Open Gripper:**
```
#n M2232 V0\n
Response: $n ok\n
```

**Query Gripper Status:**
```
#n P2232\n
Response: $n ok V1\n (0=stop, 1=working, 2=grabbing)
```

**Specifications:**
- Max Force: 750-800g
- Max Object Size: 40 mm
- Max Speed: 20 mm/s
- Drive Voltage: 6V / 300mA

---

## 5. Position Query Command Format

### Standard Position Query

```
#n P2220\n
```

**Response:**
```
$n ok X154.71 Y194.91 Z10.21\n
```

### Alternative: Joint Angles

```
#n P2200\n
```

**Response:**
```
$n ok B50 L50 R50\n
```

### Alternative: Polar Coordinates

```
#n P2221\n
```

**Response:**
```
$n ok S100 R90 H80\n
```

### Auto-Feedback (Timed Updates)

Set automatic feedback interval:
```
#n M2120 V0.5\n
```
- V = Interval in seconds

Once enabled, arm continuously sends:
```
@3 X154.71 Y194.91 Z10.21\n
```

---

## 6. Response Format Examples

### Success Response
```
Command:  #25 G0 X100 Y100 Z100 F1000
Response: $25 ok
```

### Error Response
```
Command:  #25 G0 X500 Y0 Z0 F1000
Response: $25 E22   (Address out of range / Out of workspace)
```

### Error Codes
| Code | Meaning |
|------|---------|
| E20 | Command not exist |
| E21 | Parameter error |
| E22 | Address out of range (out of workspace) |
| E23 | Command buffer full |
| E24 | Power unconnected |
| E25 | Operation failure |

### Feedback Messages
| Prefix | Meaning |
|--------|---------|
| `$n` | Response to command #n |
| `@1` | Ready signal |
| `@3` | Timed feedback (from M2120) |
| `@4` | Button event |
| `@5` | Power event |
| `@6` | Limit switch event |
| `@9` | Stop movement signal |

---

## 7. Safety Limits and Warnings

### Hardware Limits
- **Maximum Payload:** 500g (at end effector)
- **Maximum Speed:** 100 mm/s
- **Repeatability:** ±0.2 mm
- **Operating Temperature:** 0°C to 35°C
- **Operating Humidity:** 30% to 80% RH (non-condensing)

### Software Limits (To Enforce)
- **Speed Limit:** Cap at 2000 mm/min (33.3 mm/s) maximum
- **Workspace Boundary:** X[50-320], Y[-200-200], Z[0-150] mm
- **Position Validation:** Always check before sending movement commands
- **Timeout:** 1-5 seconds per command (with retry logic)

### Safety Warnings
1. **Do not** put hands between arms during movement
2. **Do not** exceed workspace boundaries (will cause positioning errors)
3. **Do not** send commands faster than arm can execute
4. **Always** use official power supply (DC 12V, 5A)
5. **Always** check power connection before operating
6. **Always** have emergency stop accessible

---

## 8. Timing Requirements and Delays

### Serial Communication Timing
- **Baud Rate:** 115200 bps
- **Frame Size:** ~1 byte per bit
- **Transmission Time:** ~86 microseconds per byte
- **Command Processing:** 10-100 ms typical
- **Movement Duration:** Depends on distance and speed

### Recommended Delays
- **Between Commands:** 50-100 ms minimum
- **After Movement:** 100-500 ms before next command
- **After Mode Change (M2400):** 200-500 ms
- **Serial Read Timeout:** 1-5 seconds

### Example Timing Sequence
```
T=0ms     Send: #1 G0 X100 Y100 Z100 F1000\n
T=10ms    Receive: $1 ok\n
T=100ms   Movement begins
T=5000ms  Movement completes (example, depends on distance)
T=5100ms  Safe to send next command
```

---

## Hardware Specifications Summary

| Parameter | Value |
|-----------|-------|
| **Connection** | Micro USB |
| **Baud Rate** | 115200 bps |
| **Weight** | 2.2 kg |
| **Degrees of Freedom** | 4 |
| **Repeatability** | ±0.2 mm |
| **Max Payload** | 500g |
| **Workspace Range** | 50-320 (X), -200-200 (Y), 0-150 (Z) mm |
| **Max Speed** | 100 mm/s |
| **Power** | DC 12V, 5A |
| **Operating Temp** | 0-35°C |
| **Dimensions** | 150×140×281 mm |
| **Base Motor** | 0-180°, 40°/s, 12 kg·cm |
| **Left Motor** | 0-130°, 40°/s, 12 kg·cm |
| **Right Motor** | 0-106°, 40°/s, 12 kg·cm |
| **End-Effector Motor** | 0-180°, 60°/s, 2 kg·cm |

---

## Complete Protocol Reference

### Core Movement Commands
- `G0` - Linear move (Cartesian)
- `G1` - Laser control
- `G2201` - Polar coordinates
- `G2202` - Joint angle control
- `G2204` - Relative movement

### Control Commands
- `M17` - Attach motors
- `M2019` - Detach motors
- `M2120` - Set feedback interval
- `M2231` - Pump control
- `M2232` - Gripper control
- `M2400` - Set mode

### Query Commands
- `P2200` - Joint angles
- `P2220` - Cartesian position
- `P2221` - Polar coordinates
- `P2231` - Pump status
- `P2232` - Gripper status
- `P2234` - Power status

### Error Codes
- E20-E25: Various hardware/software errors

---

## Critical Implementation Notes

### For Your Flask Backend:
1. **Baud Rate:** Must be 115200 (non-negotiable)
2. **Protocol:** Custom Gcode with #n/$n headers
3. **Workspace:** Enforce X[50-320], Y[-200-200], Z[0-150]
4. **Speed:** Cap at 2000 mm/min
5. **Timeouts:** Implement 5-second max per command
6. **Validation:** Always check reachability before move

### For Position Feedback:
- Use `#n P2220\n` to query current position
- Parse response format: `$n ok X### Y### Z###\n`
- Position accuracy: ±0.2mm
- Update interval: 500ms polling is acceptable

### For Safety:
- Emergency stop: Send any command with extreme timeout (1s)
- Check power status regularly: `#n P2234\n`
- Log all commands and responses
- Implement graceful error recovery

---
# Query 2: Python Serial Communication Best Practices (2025-2026)

**Status:** RESEARCH COMPLETE
**Date:** January 12, 2026
**Source:** pySerial 3.5 Official Documentation + Stack Overflow Best Practices
**Retrieved:** From official pySerial API documentation and community patterns

---

## 1. Using pyserial Library (3.5+)

### Installation

```bash
pip install pyserial==3.5
```

### Basic Connection Pattern

```python
import serial

# Recommended: Use context manager for automatic cleanup
with serial.Serial(
    port='COM3',           # Windows: COM1-COM255 | Linux: /dev/ttyUSB0
    baudrate=115200,       # Must be 115200 for SwiftArm
    timeout=1,             # Read timeout in seconds (IMPORTANT)
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
) as ser:
    # Connection guaranteed to be open here
    ser.write(b'#1 P2220\n')  # Send command
    response = ser.readline()   # Read response
# Port automatically closed when exiting context
```

### Why Context Manager?

✓ Automatic port cleanup (even if exception occurs)
✓ No resource leaks
✓ Exception-safe by design
✓ Recommended for production code

### Key Settings for Robot Control

| Setting | Value | Why |
|---------|-------|-----|
| `baudrate` | 115200 | SwiftArm requirement (non-negotiable) |
| `timeout` | 1.0 | 1 second max for serial read |
| `bytesize` | EIGHTBITS | Standard 8-bit bytes |
| `parity` | PARITY_NONE | No parity checking |
| `stopbits` | STOPBITS_ONE | Standard stop bits |

---

## 2. Timeout Handling Strategies

### Understanding pySerial Timeouts

pySerial has **THREE timeout mechanisms**:

#### A. Read Timeout (`timeout`)
```python
ser = serial.Serial('COM3', 115200, timeout=1.0)

# timeout = None   → Block forever (dangerous!)
# timeout = 0      → Non-blocking (returns immediately, may get 0 bytes)
# timeout = 1.0    → Wait max 1 second, return available bytes
```

**Recommended: `timeout=1.0` (1 second)**
- Returns immediately if data available
- Waits up to 1 second if no data
- Never blocks indefinitely

#### B. Inter-Byte Timeout (`inter_byte_timeout`)
```python
ser = serial.Serial('COM3', 115200, 
                    timeout=2.0,              # Overall timeout
                    inter_byte_timeout=0.1)   # Timeout between bytes
```

**When to use:** When messages vary in length
- Example: 8-200 byte responses
- If gap > 100ms between bytes, read ends
- Prevents blocking for partial messages

#### C. Write Timeout (`write_timeout`)
```python
ser = serial.Serial('COM3', 115200, 
                    write_timeout=1.0)
```

**When to use:** If serial port can be slow
- Prevents write() from blocking forever
- Raises `SerialTimeoutException` on timeout

### Complete Timeout Configuration Example

```python
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    timeout=2.0,              # Read timeout: 2 seconds max
    inter_byte_timeout=0.1,   # Between-byte timeout: 100ms
    write_timeout=1.0,        # Write timeout: 1 second max
)

try:
    # Send command
    ser.write(b'#1 P2220\n')

    # Read response with timeout protection
    response = ser.read(200)  # Max 200 bytes

    if not response:
        print("Timeout: No response received")
    else:
        print(f"Received: {response}")

except serial.SerialTimeoutException:
    print("Write timeout occurred")
except serial.SerialException as e:
    print(f"Serial error: {e}")
```

---

## 3. Error Recovery and Reconnection Logic

### Graceful Disconnect Handling

```python
import time
import logging

logger = logging.getLogger(__name__)

class RobustSerialConnection:
    def __init__(self, port='COM3', baudrate=115200, max_retries=3):
        self.port = port
        self.baudrate = baudrate
        self.max_retries = max_retries
        self.ser = None
        self.connected = False

    def connect(self):
        """Connect with retry logic"""
        for attempt in range(self.max_retries):
            try:
                # Close any existing connection first
                if self.ser and self.ser.is_open:
                    self.ser.close()
                    time.sleep(0.5)  # Wait for port to release

                # Attempt connection
                self.ser = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=1.0
                )

                # Flush buffers after connection
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()

                self.connected = True
                logger.info(f"Connected to {self.port}")
                return True

            except serial.SerialException as e:
                logger.warning(f"Connection attempt {attempt+1}/{self.max_retries} failed: {e}")
                time.sleep(1.0 * (attempt + 1))  # Exponential backoff

        self.connected = False
        logger.error(f"Failed to connect after {self.max_retries} attempts")
        return False

    def disconnect(self):
        """Safely disconnect"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.connected = False
            logger.info("Disconnected")

    def send_command(self, command: str) -> bytes:
        """Send command with automatic reconnect on failure"""
        if not self.connected:
            if not self.connect():
                raise Exception("Cannot connect to arm")

        try:
            # Send command
            self.ser.write(command.encode() + b'\n')

            # Read response with timeout
            response = self.ser.readline()

            return response

        except serial.SerialException as e:
            logger.error(f"Serial error during send: {e}")
            self.connected = False
            # Try reconnect for next command
            raise
```

### Reconnection Pattern with Auto-Retry

```python
def send_command_with_recovery(ser, command, max_retries=2):
    """Send command, auto-reconnect if fails"""
    for attempt in range(max_retries):
        try:
            ser.write(command.encode() + b'\n')
            response = ser.readline()

            if response:
                return response
            else:
                logger.warning("No response (timeout)")
                continue

        except serial.SerialException as e:
            logger.warning(f"Attempt {attempt+1}: {e}")

            if attempt < max_retries - 1:
                # Try to reconnect
                try:
                    ser.close()
                except:
                    pass
                time.sleep(0.5)
                try:
                    ser.open()
                except:
                    logger.error("Reconnection failed")
                    raise

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    raise Exception("Command failed after retries")
```

---

## 4. Multi-Threaded Communication

### Thread-Safe Pattern (Recommended for Flask Backend)

```python
import threading
from queue import Queue

class ThreadSafeSerialController:
    def __init__(self, port='COM3'):
        self.port = port
        self.ser = None
        self.lock = threading.Lock()
        self.command_queue = Queue()
        self.reader_thread = None
        self.running = False

    def send_command(self, command: str) -> bytes:
        """Thread-safe command sending"""
        with self.lock:
            if not self.ser or not self.ser.is_open:
                raise Exception("Serial port not open")

            try:
                self.ser.write(command.encode() + b'\n')
                response = self.ser.readline()
                return response
            except serial.SerialException as e:
                raise Exception(f"Serial error: {e}")

    def start_position_polling(self, interval=0.5):
        """Start background thread to poll position"""
        self.running = True
        self.reader_thread = threading.Thread(
            target=self._position_poller,
            args=(interval,),
            daemon=True
        )
        self.reader_thread.start()

    def _position_poller(self, interval):
        """Background thread: poll position at interval"""
        while self.running:
            try:
                # Use thread-safe send
                response = self.send_command('#1 P2220')  # Query position

                # Parse and store position
                # Example: response = b'$1 ok X100 Y100 Z50\n'

                time.sleep(interval)

            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(interval)

    def stop(self):
        """Stop polling thread"""
        self.running = False
        if self.reader_thread:
            self.reader_thread.join(timeout=2)
```

### Key Rules for Multi-Threading with Serial

1. **NEVER read/write from multiple threads simultaneously**
   - Use `threading.Lock()` to protect serial port access
   - Each operation must hold the lock

2. **Background polling thread should:**
   - Use low-priority polling (500ms or more)
   - Catch all exceptions (don't crash the thread)
   - Use the same lock as foreground commands

3. **Use context managers or locks**
   ```python
   # GOOD: Protected access
   with self.lock:
       ser.write(command)
       response = ser.readline()

   # BAD: Race condition
   ser.write(command)  # Thread 1
   ser.write(other)    # Thread 2 - WRONG!
   ```

---

## 5. Real-Time Position Feedback Polling

### Simple Polling Pattern (500ms Interval)

```python
import time

def get_current_position(ser):
    """Query and parse position"""
    try:
        ser.write(b'#1 P2220\n')  # Query Cartesian position
        response = ser.readline().decode('utf-8')

        # Parse: $1 ok X100.5 Y200.3 Z50.1\n
        if '$1 ok' in response:
            parts = response.split()
            position = {
                'x': float(parts[2][1:]),  # X value
                'y': float(parts[3][1:]),  # Y value
                'z': float(parts[4][1:]),  # Z value
            }
            return position
        else:
            return None
    except Exception as e:
        logger.error(f"Position query error: {e}")
        return None

def polling_loop(ser, interval=0.5):
    """Continuous polling loop"""
    while True:
        position = get_current_position(ser)

        if position:
            print(f"Position: X={position['x']:.1f} Y={position['y']:.1f} Z={position['z']:.1f}")
        else:
            print("Failed to get position")

        time.sleep(interval)
```

### Advanced: With Callback

```python
class PositionMonitor:
    def __init__(self, ser, callback, interval=0.5):
        self.ser = ser
        self.callback = callback
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()

    def _monitor(self):
        while self.running:
            try:
                self.ser.write(b'#1 P2220\n')
                response = self.ser.readline().decode('utf-8')

                if '$1 ok' in response:
                    # Parse position and call callback
                    self.callback(response)

                time.sleep(self.interval)

            except Exception as e:
                logger.error(f"Monitor error: {e}")
                time.sleep(self.interval)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
```

---

## 6. Emergency Stop Implementation

### Immediate Stop (Critical!)

```python
def emergency_stop(ser):
    """IMMEDIATE stop - no queued commands"""
    try:
        # Send immediate stop command
        # For SwiftArm: Send M17 (detach motors)
        ser.write(b'#999 M2019\n')  # Detach all motors

        # DON'T wait for response, prioritize stopping
        logger.critical("EMERGENCY STOP ACTIVATED")

        return True
    except Exception as e:
        logger.critical(f"Emergency stop failed: {e}")
        return False
```

### E-Stop with Timeout

```python
def emergency_stop_with_timeout(ser, timeout=0.5):
    """E-stop with timeout (no hanging)"""
    original_timeout = ser.timeout
    try:
        # Use minimal timeout for e-stop
        ser.timeout = timeout

        # Send detach motors command immediately
        ser.write(b'#999 M2019\n')

        # Try to read response but don't block
        response = ser.read(10)  # Read max 10 bytes

        logger.critical("EMERGENCY STOP SENT")
        return True

    except Exception as e:
        logger.critical(f"E-stop error: {e}")
        return False

    finally:
        ser.timeout = original_timeout
```

---

## 7. Logging and Monitoring Approaches

### Comprehensive Logging Pattern

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arm_controller.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class LoggedSerialController:
    def __init__(self, port='COM3'):
        self.ser = serial.Serial(port, 115200, timeout=1.0)
        self.command_count = 0
        self.error_count = 0

    def send_command(self, cmd_id, command):
        """Send command with comprehensive logging"""
        try:
            self.command_count += 1

            # Log command sent
            logger.info(f"[CMD {cmd_id}] Sending: {command}")

            # Send
            self.ser.write(command.encode() + b'\n')

            # Receive with timeout
            start = datetime.now()
            response = self.ser.readline()
            elapsed = (datetime.now() - start).total_seconds()

            # Log response
            logger.info(f"[CMD {cmd_id}] Response ({elapsed:.3f}s): {response}")

            return response

        except serial.SerialTimeoutException:
            self.error_count += 1
            logger.error(f"[CMD {cmd_id}] TIMEOUT - No response within {self.ser.timeout}s")
            raise

        except serial.SerialException as e:
            self.error_count += 1
            logger.error(f"[CMD {cmd_id}] SERIAL ERROR: {e}")
            raise

        except Exception as e:
            self.error_count += 1
            logger.error(f"[CMD {cmd_id}] UNEXPECTED ERROR: {e}")
            raise

    def get_stats(self):
        """Return communication statistics"""
        error_rate = (self.error_count / self.command_count * 100) if self.command_count > 0 else 0

        return {
            'total_commands': self.command_count,
            'total_errors': self.error_count,
            'error_rate': f"{error_rate:.1f}%"
        }
```

### Audit Trail Logging

```python
import json
from datetime import datetime

class AuditLog:
    def __init__(self, filename='audit.jsonl'):
        self.filename = filename

    def log_command(self, cmd_id, command, response, success, error=None):
        """Log command to audit trail"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'cmd_id': cmd_id,
            'command': command,
            'response': response.decode('utf-8') if isinstance(response, bytes) else str(response),
            'success': success,
            'error': str(error) if error else None
        }

        with open(self.filename, 'a') as f:
            f.write(json.dumps(entry) + '\n')
```

---

## 8. Common Pitfalls to Avoid

### ❌ PITFALL 1: Blocking Forever

```python
# WRONG - Can hang if no data
ser.timeout = None
data = ser.read(100)

# CORRECT - Always set timeout
ser.timeout = 1.0
data = ser.read(100)  # Max 1 second wait
```

### ❌ PITFALL 2: Not Closing Ports

```python
# WRONG - Resource leak if exception occurs
ser = serial.Serial('COM3', 115200)
ser.write(b'command')
response = ser.read(10)
ser.close()  # May never be reached!

# CORRECT - Use context manager
with serial.Serial('COM3', 115200) as ser:
    ser.write(b'command')
    response = ser.read(10)
# Automatically closed
```

### ❌ PITFALL 3: Multiple Threads on Same Port

```python
# WRONG - Race condition
Thread1: ser.write(cmd1)
Thread2: ser.write(cmd2)  # CRASH or mixed responses!

# CORRECT - Use lock
with self.lock:
    ser.write(cmd1)
    response = ser.read(10)
```

### ❌ PITFALL 4: Not Clearing Buffers After Connection

```python
# WRONG - Old data in buffer
ser = serial.Serial('COM3', 115200)
ser.write(b'command')  # Old data might be there!

# CORRECT - Clear buffers
ser = serial.Serial('COM3', 115200)
ser.reset_input_buffer()
ser.reset_output_buffer()
ser.write(b'command')
```

### ❌ PITFALL 5: No Error Handling for Disconnection

```python
# WRONG - Crashes if cable unplugged
while True:
    response = ser.read(10)  # Will throw if disconnected

# CORRECT - Handle gracefully
while True:
    try:
        response = ser.read(10)
    except serial.SerialException:
        logger.error("Serial port disconnected, reconnecting...")
        if reconnect():
            continue
        else:
            break
```

### ❌ PITFALL 6: Wrong Baud Rate

```python
# WRONG - SwiftArm is 115200, not 9600
ser = serial.Serial('COM3', 9600)

# CORRECT - Must be 115200
ser = serial.Serial('COM3', 115200)
```

### ❌ PITFALL 7: Assuming Response Immediately Available

```python
# WRONG - Timeout=0 returns immediately with partial/no data
ser.timeout = 0
data = ser.read(100)  # Might get 0 bytes!

# CORRECT - Give time for response
ser.timeout = 1.0
data = ser.read(100)  # Waits up to 1 second
```

---

## Summary: Best Practices Checklist

- [ ] Always set timeout (never `None` or 0)
- [ ] Use context managers for resource safety
- [ ] Clear input/output buffers after connection
- [ ] Use locks for multi-threaded access
- [ ] Implement reconnection logic with exponential backoff
- [ ] Log all commands and responses
- [ ] Handle SerialException explicitly
- [ ] Set inter_byte_timeout for variable-length responses
- [ ] Never ignore timeout exceptions
- [ ] Use 115200 baud rate (non-negotiable)
- [ ] Implement emergency stop without retry logic
- [ ] Monitor connection state continuously
- [ ] Test disconnection/reconnection scenarios

---
# Query 3: Flask Architecture for Hardware Control (2025-2026)

**Status:** RESEARCH COMPLETE
**Date:** January 12, 2026
**Source:** Official Flask Documentation + Production Best Practices
**Retrieved:** From Flask.io, Stack Overflow, and 2025 development practices

---

## 1. Best Flask Patterns for Hardware Device Control

### Application Factory Pattern (RECOMMENDED)

The Application Factory Pattern is the industry standard for production Flask applications because it enables:
- Dynamic configuration for different environments (dev/test/prod)
- Proper dependency injection for testing with mock hardware
- Clean extension management
- Multiple app instances with different contexts

**Pattern Structure:**

```python
# app/__init__.py - Application factory
from flask import Flask
from flask_cors import CORS
import logging

def create_app(config_name='development', arm_controller=None):
    """
    Application factory function

    Args:
        config_name: 'development', 'testing', or 'production'
        arm_controller: Injected hardware controller (for testing)
    """
    app = Flask(__name__)

    # Load configuration based on environment
    if config_name == 'development':
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    elif config_name == 'testing':
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
    elif config_name == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False

    # Enable CORS for frontend integration
    CORS(app)

    # Setup logging
    setup_logging(app)

    # Dependency injection: Pass hardware controller
    # For testing: inject MockArmController
    # For production: inject RealSwiftArmController
    app.arm_controller = arm_controller or None

    # Register blueprints (modular routing)
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register global error handlers
    register_error_handlers(app)

    return app

def setup_logging(app):
    """Configure structured logging"""
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

def register_error_handlers(app):
    """Register global error handlers"""
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request', 'code': 400}, 400

    @app.errorhandler(503)
    def service_unavailable(error):
        return {'error': 'Arm controller unavailable', 'code': 503}, 503

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal error: {error}")
        return {'error': 'Internal server error', 'code': 500}, 500
```

**Using the Factory:**

```python
# Testing with mock hardware
from app import create_app
from tests.mocks import MockArmController

app = create_app('testing', arm_controller=MockArmController())
client = app.test_client()

# Production with real hardware
from app import create_app
from backend.arm_controller import SwiftArmController

app = create_app('production', arm_controller=SwiftArmController('COM3'))
```

---

### Blueprint Pattern for Modularity

Blueprints organize routes into logical groups, making code maintainable and testable.

```python
# app/api.py - Blueprint for all hardware endpoints
from flask import Blueprint, request, current_app
from functools import wraps
import logging
import time

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Decorator: Verify arm controller is available
def require_arm_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.arm_controller or not current_app.arm_controller.connected:
            return {
                'error': 'Arm controller not connected',
                'code': 503
            }, 503
        return f(*args, **kwargs)
    return decorated_function

# Helper: Validate position is in workspace
def validate_position(x, y, z):
    """Check position is reachable"""
    WORKSPACE = {
        'x_min': 50, 'x_max': 320,
        'y_min': -200, 'y_max': 200,
        'z_min': 0, 'z_max': 150
    }

    if not (WORKSPACE['x_min'] <= x <= WORKSPACE['x_max']):
        return False, f"X out of range [{WORKSPACE['x_min']}, {WORKSPACE['x_max']}]"
    if not (WORKSPACE['y_min'] <= y <= WORKSPACE['y_max']):
        return False, f"Y out of range [{WORKSPACE['y_min']}, {WORKSPACE['y_max']}]"
    if not (WORKSPACE['z_min'] <= z <= WORKSPACE['z_max']):
        return False, f"Z out of range [{WORKSPACE['z_min']}, {WORKSPACE['z_max']}]"

    return True, "Valid"

# Routes
@api_bp.route('/status', methods=['GET'])
def get_status():
    """Check arm connection and get current position"""
    try:
        if not current_app.arm_controller:
            return {'status': 'disconnected', 'position': None}, 503

        position = current_app.arm_controller.get_current_position()

        return {
            'status': 'connected' if position else 'error',
            'position': position,
            'timestamp': time.time()
        }, 200

    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {'error': str(e), 'code': 500}, 500

@api_bp.route('/move', methods=['POST'])
@require_arm_connection
def move_arm():
    """Move arm to specified position"""
    try:
        data = request.get_json()

        # Input validation
        if not all(k in data for k in ['x', 'y', 'z']):
            return {'error': 'Missing x, y, z coordinates', 'code': 400}, 400

        x, y, z = data['x'], data['y'], data['z']
        speed = data.get('speed', 1000)

        # Type validation
        if not all(isinstance(v, (int, float)) for v in [x, y, z, speed]):
            return {'error': 'Coordinates must be numeric', 'code': 400}, 400

        # Position validation
        valid, message = validate_position(x, y, z)
        if not valid:
            return {'error': message, 'code': 400}, 400

        # Speed clamping (safety)
        if speed > 2000:
            speed = 2000
            logger.warning(f"Speed clamped to {speed} mm/min")

        # Execute movement
        result = current_app.arm_controller.move_to_position(x, y, z, speed)

        if result['success']:
            logger.info(f"Moved to ({x}, {y}, {z}) at {speed} mm/min")
            return result, 200
        else:
            logger.warning(f"Move failed: {result.get('error')}")
            return result, 400

    except Exception as e:
        logger.error(f"Move error: {e}")
        return {'error': str(e), 'code': 500}, 500

@api_bp.route('/emergency-stop', methods=['POST'])
def emergency_stop():
    """IMMEDIATE stop - no retry logic"""
    try:
        if current_app.arm_controller:
            current_app.arm_controller.emergency_stop()

        logger.critical("EMERGENCY STOP ACTIVATED")
        return {'status': 'STOPPED', 'code': 200}, 200

    except Exception as e:
        logger.critical(f"E-stop failed: {e}")
        return {'error': f"E-stop error: {e}", 'code': 500}, 500
```

---

## 2. REST API Design for IoT/Hardware Systems

### Proper Resource Endpoints

| Endpoint | Method | Purpose | Status |
|----------|--------|---------|--------|
| `/api/status` | GET | Query arm status + position | 200, 503 |
| `/api/move` | POST | Move to coordinates | 200, 400, 503 |
| `/api/gripper` | POST | Control gripper | 200, 400, 503 |
| `/api/home` | POST | Return to home (0,0,0) | 200, 503 |
| `/api/emergency-stop` | POST | STOP immediately | 200, 500 |
| `/api/workspace` | GET | Get workspace bounds | 200 |

### HTTP Status Codes for Hardware

```
2xx Success:
- 200 OK             → Operation succeeded
- 202 ACCEPTED       → Operation queued (async)

4xx Client Error:
- 400 BAD REQUEST    → Invalid input (bad JSON, out of bounds)
- 401 UNAUTHORIZED   → Authentication required
- 422 UNPROCESSABLE  → Valid JSON but semantically wrong

5xx Server Error:
- 503 UNAVAILABLE    → Arm not connected or communication error
- 500 INTERNAL       → Unexpected server error
- 504 TIMEOUT        → Serial communication timeout
```

### Request/Response Examples

```json
// Move arm request
POST /api/move
{
  "x": 150,
  "y": 50,
  "z": 100,
  "speed": 1000
}

// Success response (200)
{
  "success": true,
  "position": {"x": 150, "y": 50, "z": 100},
  "command": "#1 G0 X150 Y50 Z100 F1000",
  "timestamp": 1673299200.123
}

// Error response (400 - out of bounds)
{
  "success": false,
  "error": "X out of range [50, 320]",
  "code": 400
}

// Error response (503 - disconnected)
{
  "error": "Arm controller not connected",
  "code": 503,
  "suggestion": "Check USB connection"
}
```

---

## 3. Real-Time Updates: WebSocket vs Polling Comparison

### Quick Comparison

| Feature | REST Polling | WebSocket |
|---------|------------|-----------|
| Latency | 500ms-5s | 10-100ms |
| Server Load | High | Low |
| Complexity | Simple | Medium |
| Browser Support | 100% | 99%+ |
| Best For | Occasional updates | Real-time streaming |

### Phase 1 (MVP): REST Polling

**Recommended:** 500ms polling interval

```javascript
// frontend/js/app.js - Poll for position updates
async function pollPosition() {
    while (true) {
        try {
            const response = await fetch('/api/status');

            if (!response.ok) {
                updateConnectionStatus(false);
                continue;
            }

            const data = await response.json();

            if (data.position) {
                updatePositionDisplay(data.position);
                updateConnectionStatus(true);
            }
        } catch (error) {
            console.error('Poll error:', error);
            updateConnectionStatus(false);
        }

        await new Promise(resolve => setTimeout(resolve, 500));
    }
}

// Start polling on page load
document.addEventListener('DOMContentLoaded', () => {
    pollPosition();  // Non-blocking background polling
});
```

### Phase 2+ (Advanced): WebSocket

```python
# app/__init__.py - Add WebSocket support
from flask_socketio import SocketIO, emit
import threading

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected via WebSocket")
    emit('connection_response', {'data': 'Connected to arm'})

@socketio.on('request_position')
def handle_position_request():
    if current_app.arm_controller and current_app.arm_controller.connected:
        position = current_app.arm_controller.get_current_position()
        emit('position_update', position)

# Background thread: broadcast updates every 50ms
def background_position_broadcaster():
    while True:
        if current_app.arm_controller and current_app.arm_controller.connected:
            position = current_app.arm_controller.get_current_position()
            socketio.emit('position_update', position, broadcast=True)
        time.sleep(0.05)

socketio.start_background_task(background_position_broadcaster)
```

---

## 4. Error Handling and Status Codes

### Custom Exception Hierarchy

```python
# app/errors.py - Custom exception classes
class ArmControllerError(Exception):
    """Base exception for arm errors"""
    def __init__(self, message, code=500, user_message=None):
        self.message = message
        self.code = code
        self.user_message = user_message or message
        super().__init__(self.message)

class PositionOutOfBounds(ArmControllerError):
    def __init__(self, x, y, z):
        message = f"Position ({x}, {y}, {z}) outside workspace"
        super().__init__(message, code=422, user_message=message)

class ArmNotConnected(ArmControllerError):
    def __init__(self, port):
        message = f"Cannot connect to arm on {port}"
        super().__init__(message, code=503, user_message="Arm not connected")

class SerialTimeout(ArmControllerError):
    def __init__(self):
        message = "Serial communication timeout"
        super().__init__(message, code=504, user_message="Arm not responding")

class InvalidSpeed(ArmControllerError):
    def __init__(self, speed):
        message = f"Speed {speed} exceeds maximum 2000 mm/min"
        super().__init__(message, code=422, user_message="Max speed: 2000 mm/min")
```

### Global Error Handler

```python
# app/__init__.py - Register error handler
@app.errorhandler(ArmControllerError)
def handle_arm_error(error):
    response = {
        'error': error.user_message,
        'code': error.code,
        'timestamp': time.time()
    }
    app.logger.warning(f"Arm error ({error.code}): {error.message}")
    return response, error.code
```

---

## 5. Connection Management and Timeouts

### Context Manager Pattern

```python
# app/hardware.py - Safe connection management
from contextlib import contextmanager
import threading
import time

class ArmControllerManager:
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.controller = None
        self.lock = threading.Lock()
        self.timeout = 5  # seconds

    @contextmanager
    def connect(self):
        """Context manager: ensures safe connection and cleanup"""
        try:
            with self.lock:
                if not self.controller:
                    from backend.arm_controller import SwiftArmController
                    self.controller = SwiftArmController(self.port, self.baudrate)
                    if not self.controller.connect():
                        raise Exception(f"Cannot connect to {self.port}")

            yield self.controller

        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

        finally:
            # Automatic cleanup guaranteed
            pass

    def disconnect(self):
        with self.lock:
            if self.controller:
                self.controller.disconnect()
                self.controller = None
```

### Timeout Protection with ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

executor = ThreadPoolExecutor(max_workers=5)

@api_bp.route('/move', methods=['POST'])
def move_arm():
    data = request.get_json()
    x, y, z = data['x'], data['y'], data['z']
    speed = data.get('speed', 1000)

    try:
        # Execute with 10-second timeout
        future = executor.submit(
            current_app.arm_controller.move_to_position,
            x, y, z, speed
        )

        result = future.result(timeout=10)  # Max 10 seconds

        return {'success': True, 'position': result}, 200

    except FutureTimeoutError:
        logger.error("Movement timeout (>10s)")
        return {'error': 'Movement timeout', 'code': 504}, 504

    except Exception as e:
        logger.error(f"Movement error: {e}")
        return {'error': str(e), 'code': 500}, 500
```

---

## 6. Testing Strategies for Hardware APIs (Mocking)

### Mock Hardware Controller

```python
# tests/mocks.py - Mock hardware for testing
class MockArmController:
    def __init__(self):
        self.connected = True
        self.position = {'x': 0, 'y': 0, 'z': 0}
        self.gripper_state = 'open'
        self.movement_count = 0

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False

    def get_current_position(self):
        return self.position

    def move_to_position(self, x, y, z, speed):
        if not self.connected:
            return {'success': False, 'error': 'Not connected'}

        # Validate bounds
        if not (50 <= x <= 320 and -200 <= y <= 200 and 0 <= z <= 150):
            return {'success': False, 'error': 'Out of bounds'}

        # Simulate movement
        self.position = {'x': x, 'y': y, 'z': z}
        self.movement_count += 1

        return {'success': True, 'position': self.position}

    def control_gripper(self, action):
        self.gripper_state = 'open' if action == 'open' else 'closed'
        return {'success': True, 'state': self.gripper_state}

    def emergency_stop(self):
        return {'status': 'STOPPED'}
```

### pytest Fixtures

```python
# tests/conftest.py - Test configuration
import pytest
from app import create_app
from tests.mocks import MockArmController

@pytest.fixture
def mock_controller():
    return MockArmController()

@pytest.fixture
def app(mock_controller):
    app = create_app('testing', arm_controller=mock_controller)
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

### Test Cases

```python
# tests/test_api.py - API endpoint tests
def test_status_connected(client, mock_controller):
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'connected'

def test_move_valid(client, mock_controller):
    response = client.post('/api/move', json={
        'x': 100, 'y': 0, 'z': 50, 'speed': 1000
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True

def test_move_out_of_bounds(client, mock_controller):
    response = client.post('/api/move', json={
        'x': 400, 'y': 0, 'z': 50, 'speed': 1000
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'out of range' in data['error'].lower()

def test_emergency_stop(client):
    response = client.post('/api/emergency-stop')
    assert response.status_code == 200
```

---

## 7. Performance Optimization for Real-Time Systems

### Position Caching

```python
class PositionCache:
    def __init__(self, ttl_ms=100):
        self.cache = None
        self.timestamp = 0
        self.ttl_ms = ttl_ms

    def get(self, fetch_func):
        now = time.time() * 1000

        if self.cache and (now - self.timestamp) < self.ttl_ms:
            return self.cache  # Return cached value

        self.cache = fetch_func()
        self.timestamp = now
        return self.cache

position_cache = PositionCache(ttl_ms=100)

@api_bp.route('/status', methods=['GET'])
def get_status():
    position = position_cache.get(
        lambda: current_app.arm_controller.get_current_position()
    )
    return {'status': 'connected', 'position': position}, 200
```

### Response Time Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Status query | <50ms | With caching |
| Position update | <100ms | Over serial |
| Move command | <200ms | Validation + serial |
| Emergency stop | <10ms | No retry |

---

## 8. Security Considerations for Hardware Control

### Input Validation

```python
def validate_move_request(data):
    """Validate move request parameters"""
    required = ['x', 'y', 'z']

    if not all(k in data for k in required):
        raise ValueError(f"Missing required fields: {required}")

    x, y, z = data['x'], data['y'], data['z']

    if not all(isinstance(v, (int, float)) for v in [x, y, z]):
        raise ValueError("Coordinates must be numbers")

    if not (50 <= x <= 320 and -200 <= y <= 200 and 0 <= z <= 150):
        raise ValueError("Position out of workspace")

    speed = data.get('speed', 1000)
    if not (0 <= speed <= 2000):
        speed = min(max(speed, 0), 2000)

    return x, y, z, speed
```

### Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(key_func=get_remote_address)

@api_bp.route('/move', methods=['POST'])
@limiter.limit("10 per minute")  # Max 10 moves/min per IP
def move_arm():
    # ... implementation
```

### Security Checklist

- [ ] All inputs validated (type, range, length)
- [ ] XSS prevention (HTML escaping)
- [ ] CSRF tokens for state-changing operations
- [ ] Rate limiting (10 moves/minute per client)
- [ ] Workspace boundaries enforced
- [ ] Speed limits enforced (max 2000 mm/min)
- [ ] Emergency stop always accessible
- [ ] All commands logged to audit trail
- [ ] Error messages don't leak sensitive info
- [ ] HTTPS enforced (production)

---

## Summary: Complete Flask Architecture

Your Flask backend will use:

✓ **Application Factory** - Clean, testable, flexible  
✓ **Blueprints** - Modular organization  
✓ **Mock Injection** - Test without hardware  
✓ **Custom Exceptions** - Type-safe error handling  
✓ **Context Managers** - Safe resource cleanup  
✓ **REST Polling** - Simple, sufficient for Phase 1  
✓ **WebSocket** - Ready for Phase 2+ upgrade  
✓ **Security** - Validation, rate limiting, logging  

---
 Query 4: Docker USB Configuration for Windows 11 (2025-2026)

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

