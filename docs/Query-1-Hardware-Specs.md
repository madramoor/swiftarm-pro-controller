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

**Document:** Query 1 - SwiftArm Pro Hardware Specifications (COMPLETE)
**Status:** Ready for backend development
**Last Updated:** January 12, 2026
**Source:** Official uArm Developer Guide v1.0.6 + Quick Start Guide
