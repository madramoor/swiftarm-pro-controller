"""Mock hardware controller for testing"""


class MockArmController:
    """Mock controller - no real hardware"""

    WORKSPACE = {
        'x_min': 50, 'x_max': 320,
        'y_min': -200, 'y_max': 200,
        'z_min': 0, 'z_max': 150,
    }

    def __init__(self):
        self.connected = True
        self.position = {'x': 0, 'y': 0, 'z': 0}
        self.gripper = 'open'
        self.pump = 'off'
        self.move_count = 0

    def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False

    def get_current_position(self):
        if not self.connected:
            return None
        return self.position

    def move_to_position(self, x, y, z, speed=1000):
        if not (self.WORKSPACE['x_min'] <= x <= self.WORKSPACE['x_max']):
            return {'success': False, 'error': 'X out of range'}
        if not (self.WORKSPACE['y_min'] <= y <= self.WORKSPACE['y_max']):
            return {'success': False, 'error': 'Y out of range'}
        if not (self.WORKSPACE['z_min'] <= z <= self.WORKSPACE['z_max']):
            return {'success': False, 'error': 'Z out of range'}

        speed = min(max(speed, 1), 2000)

        if not self.connected:
            return {'success': False, 'error': 'Not connected'}

        self.position = {'x': x, 'y': y, 'z': z}
        self.move_count += 1
        return {'success': True, 'position': self.position}

    def control_gripper(self, action):
        if not self.connected:
            return {'success': False}
        self.gripper = action
        return {'success': True, 'state': action}

    def control_pump(self, state):
        if not self.connected:
            return {'success': False}
        self.pump = 'on' if state else 'off'
        return {'success': True, 'state': state}

    def emergency_stop(self):
        return {'status': 'STOPPED'}
