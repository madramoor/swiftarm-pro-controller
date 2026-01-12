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

**Document:** Query 3 - Flask Architecture for Hardware Control (COMPLETE)
**Status:** Ready for backend implementation
**Last Updated:** January 12, 2026
**Source:** Official Flask Docs 3.1.x + Production Best Practices 2025
