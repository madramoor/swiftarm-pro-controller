# SwiftArm Pro Flask Backend

Production-grade Flask REST API for SwiftArm Pro robot arm control.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Docker (Windows 11)

```bash
docker-compose up
```

## Testing

```bash
pytest --cov=app --cov=backend --cov-report=term-missing
```

Target: 85%+ coverage

## API Endpoints

- GET `/api/status` - Arm status and position
- POST `/api/move` - Move to coordinates
- POST `/api/gripper` - Control gripper
- POST `/api/pump` - Control pump
- POST `/api/emergency-stop` - Stop immediately
- GET `/api/workspace` - Workspace bounds

## Architecture

- Application Factory pattern
- Mock hardware for testing
- Thread-safe serial communication
- Comprehensive error handling
