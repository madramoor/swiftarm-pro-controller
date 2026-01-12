TASK NAME: SwiftArm Pro Backend Core Generation

PROJECT CONTEXT:
- Repository: E:\Code\SwiftArm\swiftarm-pro-controller
  (Windows path - Agent Zero will detect and work with local files)
- GitHub Repo: https://github.com/madramoor/swiftarm-pro-controller
- Device: SwiftArm Pro robot arm (USB serial, 115200 baud)
- Development Environment: Windows 11 with Docker Desktop
- Test Environment: Docker container with USB device mapping

HARDWARE SPECIFICATIONS (From Perplexity Research):
- USB Connection: COM port (Windows) mapped to /dev/ttyUSB0 in Docker
- Baud Rate: 115200
- Gcode Format: #0 [COMMAND] [PARAMETERS]
- Response Format: $0 ok [DATA] or error code
- Workspace Limits: X[0-300mm], Y[-200-200mm], Z[0-150mm]
- Speed Limit: Max 2000 mm/min
- Movement Command: #0 G0 X{x} Y{y} Z{z} F{speed}
- Gripper Command: #0 M2231 V{0 or 1} (0=release, 1=grasp)
- Position Query: #0 P2220 (returns position)
- Home Command: #0 G0 X0 Y0 Z0 F1000

REQUIRED FILES TO CREATE:

1. backend/arm_controller.py
   - Class: SwiftArmController
   - Methods:
     * __init__(port, baudrate) - Initialize with serial port
     * connect() → bool - Establish USB connection, return success
     * disconnect() - Close connection safely
     * send_command(cmd: str) → str - Send command, get response
     * move_to_position(x, y, z, speed=1000) → dict - Move arm safely
     * get_current_position() → dict - Query current position
     * control_gripper(open: bool) → str - Control gripper
     * emergency_stop() → str - Stop all movement
     * validate_position(x, y, z) → bool - Check workspace limits
   - Error Handling:
     * Connection timeout (1 second)
     * Disconnection and auto-reconnect
     * Invalid position (outside workspace)
     * Serial port not found
     * Malformed responses
   - Logging: Log all commands, responses, errors
   - Type hints on all functions
   - Docstrings for all methods
   - Thread-safe serial communication

2. backend/gcode_generator.py
   - Class: GcodeGenerator
   - Static Methods:
     * pick_and_place(pickup_xyz, dropoff_xyz, height) → List[str]
       Returns: Sequence of move commands for pick-and-place operation
     * home_position() → List[str]
       Returns: Commands to move to home (0,0,0)
     * calibration_sequence() → List[str]
       Returns: Arm calibration commands (reference homing)
   - Functions:
     * generate_linear_path(start, end, steps) → List[str]
       Returns: Intermediate waypoints for smooth movement
     * validate_trajectory(commands) → bool
       Validates all commands are within workspace
   - Include actual Gcode command generation
   - All commands must pass workspace validation

3. backend/app.py (Flask REST API)
   - Framework: Flask with Flask-CORS
   - Port: 5000
   - Endpoints:
     * GET /api/status
       Returns: {status: "connected"/"disconnected", position: {x,y,z}}
     * POST /api/move
       Body: {x, y, z, speed}
       Returns: {success: bool, command: str, response: str}
     * POST /api/gripper
       Body: {open: bool}
       Returns: {success: bool, state: "open"/"closed"}
     * POST /api/pick-and-place
       Body: {pickup: [x,y,z], dropoff: [x,y,z]}
       Returns: {success: bool, commands_executed: int, results: [...]}
     * POST /api/home
       Returns: {success: bool, message: str}
     * POST /api/calibrate
       Returns: {success: bool, steps_executed: int}
     * POST /api/emergency-stop
       Returns: {success: bool, message: "STOPPED"}
     * GET /api/workspace
       Returns: {x_min, x_max, y_min, y_max, z_min, z_max}
   - CORS: Enable for localhost testing
   - Error Handling:
     * 400: Bad request (missing parameters, invalid input)
     * 503: Service unavailable (arm not connected)
     * 500: Internal server error (unexpected error)
   - Input Validation:
     * Check all coordinates are within workspace
     * Validate speed is between 0-2000
     * Validate data types
   - Logging: Log every API call and response

4. backend/requirements.txt
   Flask==2.3.0
   Flask-CORS==4.0.0
   pyserial==3.5
   python-dotenv==1.0.0
   pytest==7.4.0
   pytest-cov==4.0.0
   Werkzeug==2.3.0

5. backend/tests/test_arm_controller.py
   - Unit tests using pytest
   - Mock serial.Serial for testing without hardware
   - Test Cases:
     * test_connect_success - Successful connection
     * test_connect_failure - Port not found
     * test_send_command - Command sent and response received
     * test_move_to_position - Valid position movement
     * test_move_outside_workspace - Rejected position (safety)
     * test_speed_limit - Speed capped at 2000
     * test_timeout_handling - Timeout recovery
     * test_gripper_control - Gripper open/close
     * test_emergency_stop - Emergency stop
     * test_position_parsing - Response parsing accuracy
   - Mock all serial communication
   - Aim for 85%+ code coverage
   - Include test fixtures for common scenarios

6. backend/tests/test_app.py
   - Flask API endpoint tests
   - Test each REST endpoint
   - Mock arm_controller for testing
   - Test Cases:
     * test_status_endpoint - Returns status
     * test_move_endpoint - Valid move returns 200
     * test_move_invalid_position - Returns 400
     * test_move_disconnected - Returns 503
     * test_pick_and_place - Full sequence executes
     * test_gripper_endpoints - Open/close work
     * test_workspace_validation - Rejects out-of-bounds
   - Use pytest fixtures
   - Test error handling

7. backend/tests/test_gcode_generator.py
   - Test Gcode generation
   - Test Cases:
     * test_pick_and_place_sequence - Correct command order
     * test_workspace_validation - All commands valid
     * test_linear_path_generation - Smooth intermediate waypoints
     * test_home_position - Returns home commands
   - Validate command format

8. docker/Dockerfile
   - Base: python:3.11-slim
   - Install system dependencies:
     * build-essential
     * python3-dev
   - Copy requirements.txt and install
   - Copy backend/ code
   - Expose port 5000
   - Set working directory to /app
   - CMD: python app.py
   - No hardcoded secrets or API keys

9. docker/docker-compose.yml
   - Version: 3.8+
   - Service: swiftarm-app
     * Build from ./docker/Dockerfile
     * Port mapping: 5000:5000
     * Volumes: ./backend:/app (live reload in dev)
     * Environment: FLASK_ENV=development, FLASK_APP=app.py
     * Device: Map /dev/ttyUSB0:/dev/ttyUSB0 for USB access
       (Windows users: This may need adjustment - use COM3:/dev/ttyUSB0)
     * Networks: bridge
     * Restart: unless-stopped
   - Network configuration for frontend access
   - Health check: curl http://localhost:5000/api/status every 10s

SAFETY REQUIREMENTS:
- All position commands must validate against workspace bounds
- Speed must be limited to 2000 mm/min maximum
- Emergency stop must be instantaneous (no queued commands)
- Timeout on serial reads: 1 second
- Reconnection logic: Auto-attempt reconnect if disconnected
- Every command logged with timestamp and response

CODE QUALITY:
- Type hints on all functions (Python 3.11+)
- Docstrings for all classes and public methods
- Follow PEP 8 style guide
- No magic numbers - use constants
- Clear error messages (not cryptic codes)
- Comprehensive error handling

EXECUTION STEPS:
1. Create all files listed above in correct locations
2. Write all code (don't skip files)
3. Run: pytest backend/tests/ --cov --cov-report=term-missing
4. Verify: All tests pass, coverage >= 85%
5. Run: docker build -t swiftarm-app ./docker
6. Verify: Docker build succeeds, no errors
7. Push to GitHub: git add . && git commit -m "Agent Zero: Complete backend implementation with tests" && git push
8. Report results: Show test output, coverage report, and any issues found

TESTING:
After generation, verify:
- pytest output shows all tests passing
- Coverage report shows >= 85%
- Docker build completes without errors
- No linting errors

DELIVERABLES:
- Complete working Flask REST API
- Full test suite with 85%+ coverage
- Production-ready error handling
- Docker container building successfully
- All code pushed to GitHub
- Summary of what was created

IMPORTANT:
- Do NOT skip the test files - they're critical for safety
- Do NOT use hardcoded values - use constants for workspace limits
- Do NOT skip error handling - robot control requires robustness
- Do NOT commit without pushing to GitHub
