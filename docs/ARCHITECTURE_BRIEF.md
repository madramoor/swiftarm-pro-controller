\# SwiftArm Pro Control Application - Architecture Brief



\## Project Overview

Build a complete web-based control application for SwiftArm Pro robot arm that:

\- Communicates via USB serial connection (115200 baud)

\- Provides real-time position feedback and control

\- Enforces safety limits and emergency stop

\- Supports pick-and-place operations

\- Runs in Docker containers (Windows 11)

\- Can be deployed locally or on Raspberry Pi



\## Technology Stack



\### Backend

\- \*\*Framework:\*\* Flask (Python, lightweight, hardware-friendly)

\- \*\*Serial:\*\* pyserial (v3.5+, USB communication)

\- \*\*Server:\*\* Gunicorn (production) or Flask dev server (development)

\- \*\*Testing:\*\* pytest with mocking for serial communication

\- \*\*Language:\*\* Python 3.11+



\### Frontend  

\- \*\*Core:\*\* HTML5/CSS3/Vanilla JavaScript (no heavy frameworks initially)

\- \*\*Real-time:\*\* REST polling (500ms intervals) or WebSocket (future)

\- \*\*3D Visualization:\*\* Three.js (optional, for arm state visualization)

\- \*\*Responsive:\*\* Mobile-first design, works on desktop/tablet/mobile



\### Deployment

\- \*\*Container:\*\* Docker with docker-compose

\- \*\*OS:\*\* Windows 11 with WSL2 (or Docker Desktop)

\- \*\*Optional:\*\* Raspberry Pi native deployment

\- \*\*CI/CD:\*\* GitHub Actions for automated testing



\## Hardware Interface



\### SwiftArm Pro Specifications

\- \*\*Connection:\*\* USB serial (/dev/ttyUSB0 on Linux, COM3+ on Windows)

\- \*\*Baud Rate:\*\* 115200

\- \*\*Protocol:\*\* Gcode with proprietary extensions (from Perplexity research)

\- \*\*Axes:\*\* X (300mm range), Y (200mm range), Z (150mm range), Rotation

\- \*\*End Effector:\*\* Pump/gripper control via M2231 command

\- \*\*Movement Range:\*\* X\[0-300], Y\[-200-200], Z\[0-150]



\### Safety Limits (Enforced in Software)

\- Maximum speed: 2000 mm/min

\- Workspace boundaries: Enforced on every move command

\- Emergency stop: Halts all movement immediately

\- Timeout: 1 second for serial communication



\## System Architecture



┌─────────────────────────────────────────────────────────┐

│ Windows 11 PC │

│ ┌───────────────────────────────────────────────────┐ │

│ │ Docker Container (Flask App) │ │

│ │ ┌──────────────────────────────────────────────┐ │ │

│ │ │ Web Browser (http://localhost:5000) │ │ │

│ │ │ ├─ Position Control Panel │ │ │

│ │ │ ├─ Gripper Controls │ │ │

│ │ │ ├─ Pick \& Place Interface │ │ │

│ │ │ └─ Movement History Log │ │ │

│ │ └──────────────────────────────────────────────┘ │ │

│ │ ↕ (REST API calls) │ │

│ │ ┌──────────────────────────────────────────────┐ │ │

│ │ │ Flask REST API (5000) │ │ │

│ │ │ ├─ /api/status (GET) │ │ │

│ │ │ ├─ /api/move (POST) │ │ │

│ │ │ ├─ /api/gripper (POST) │ │ │

│ │ │ ├─ /api/pick-and-place (POST) │ │ │

│ │ │ └─ /api/emergency-stop (POST) │ │ │

│ │ └──────────────────────────────────────────────┘ │ │

│ │ ↕ (Serial communication) │ │

│ │ ┌──────────────────────────────────────────────┐ │ │

│ │ │ Python Serial Controller (pyserial) │ │ │

│ │ │ ├─ Connection management │ │ │

│ │ │ ├─ Gcode generation │ │ │

│ │ │ ├─ Response parsing │ │ │

│ │ │ └─ Safety validation │ │ │

│ │ └──────────────────────────────────────────────┘ │ │

│ └───────────────────────────────────────────────────┘ │

│ ↕ (/dev/ttyUSB0) │

│ ┌───────────────────────────────────────────────────┐ │

│ │ SwiftArm Pro Robot Arm │ │

│ │ (Connected via USB cable, 115200 baud) │ │

│ └───────────────────────────────────────────────────┘ │

└─────────────────────────────────────────────────────────┘





\## Development Workflow



1\. \*\*Local Development on Win11\*\*

&nbsp;  - Agent Zero generates code in `swiftarm-pro-controller/` directory

&nbsp;  - Docker container runs Flask app

&nbsp;  - Web browser accesses http://localhost:5000

&nbsp;  - Agent Zero executes code to test and verify



2\. \*\*Version Control\*\*

&nbsp;  - Code pushed to GitHub after each phase

&nbsp;  - Branches for experimental features

&nbsp;  - GitHub Actions runs tests on every push



3\. \*\*Testing\*\*

&nbsp;  - Unit tests with mocked serial connection (no hardware needed)

&nbsp;  - Integration tests for API endpoints

&nbsp;  - Manual hardware testing when robot connected

&nbsp;  - Coverage target: 85%+



\## Known Constraints \& Assumptions



\- USB device mapping works in Docker on Windows 11

\- SwiftArm Pro responds to Gcode commands as documented

\- Network latency is acceptable for non-real-time applications

\- Position feedback is only requested manually (no continuous polling from arm)

\- No state persistence between restarts (stateless design)



\## Deliverables by Phase



| Phase | Days | Deliverables |

|-------|------|--------------|

| 1. Research | 1-2 | Research notes, architecture brief |

| 2. Backend Core | 3-4 | arm\_controller.py, gcode\_generator.py, tests |

| 3. Flask API | 4-5 | app.py with full REST API |

| 4. Frontend | 5-6 | index.html, CSS, JavaScript |

| 5. Testing | 6-7 | Comprehensive test suite (85%+ coverage) |

| 6. Documentation | 7-8 | README, API docs, user guide, deployment |

| 7. Deployment | 8 | Docker config, GitHub setup, release |

| 8+ | Ongoing | Advanced features (WebSocket, 3D viz, ML) |



