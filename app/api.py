"""REST API endpoints"""
from flask import Blueprint, request, current_app
import time

api_bp = Blueprint('api', __name__)


@api_bp.route('/status', methods=['GET'])
def get_status():
    """Get arm status"""
    if not current_app.arm_controller or not current_app.arm_controller.connected:
        return {
            'status': 'disconnected',
            'position': None,
            'gripper': None,
            'pump': None,
        }, 503

    pos = current_app.arm_controller.get_current_position()
    return {
        'status': 'connected',
        'position': pos,
        'gripper': current_app.arm_controller.gripper,
        'pump': current_app.arm_controller.pump,
        'timestamp': time.time()
    }, 200


@api_bp.route('/move', methods=['POST'])
def move_arm():
    """Move to position"""
    if not current_app.arm_controller or not current_app.arm_controller.connected:
        return {'error': 'Arm not connected'}, 503

    data = request.get_json()
    if not data:
        return {'error': 'No JSON provided'}, 400

    if 'x' not in data or 'y' not in data or 'z' not in data:
        return {'error': 'Missing x, y, or z'}, 400

    try:
        x = float(data['x'])
        y = float(data['y'])
        z = float(data['z'])
        speed = float(data.get('speed', 1000))
    except (ValueError, TypeError):
        return {'error': 'Invalid numeric values'}, 400

    result = current_app.arm_controller.move_to_position(x, y, z, speed)

    if result['success']:
        return {
            'success': True,
            'position': result['position'],
            'timestamp': time.time()
        }, 200
    else:
        return {'error': result.get('error', 'Move failed')}, 400


@api_bp.route('/gripper', methods=['POST'])
def control_gripper():
    """Control gripper"""
    if not current_app.arm_controller or not current_app.arm_controller.connected:
        return {'error': 'Arm not connected'}, 503

    data = request.get_json()
    action = data.get('action', 'open') if data else 'open'

    if action not in ['open', 'close']:
        return {'error': 'Action must be open or close'}, 400

    result = current_app.arm_controller.control_gripper(action)
    return result, 200 if result['success'] else 503


@api_bp.route('/pump', methods=['POST'])
def control_pump():
    """Control pump"""
    if not current_app.arm_controller or not current_app.arm_controller.connected:
        return {'error': 'Arm not connected'}, 503

    data = request.get_json()
    state = int(data.get('state', 0)) if data else 0

    result = current_app.arm_controller.control_pump(state)
    return result, 200 if result['success'] else 503


@api_bp.route('/emergency-stop', methods=['POST'])
def emergency_stop():
    """Emergency stop"""
    if current_app.arm_controller:
        result = current_app.arm_controller.emergency_stop()
    else:
        result = {'status': 'STOPPED'}

    return result, 200


@api_bp.route('/workspace', methods=['GET'])
def get_workspace():
    """Get workspace bounds"""
    return {
        'x_min': 50,
        'x_max': 320,
        'y_min': -200,
        'y_max': 200,
        'z_min': 0,
        'z_max': 150,
    }, 200
