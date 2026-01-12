"""SwiftArm Pro Hardware Controller"""
import serial
import threading
import time
import logging

logger = logging.getLogger(__name__)


class SwiftArmController:
    """Real hardware controller via USB serial"""

    WORKSPACE = {
        'x_min': 50, 'x_max': 320,
        'y_min': -200, 'y_max': 200,
        'z_min': 0, 'z_max': 150,
    }

    def __init__(self, port='COM3', baudrate=115200, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.lock = threading.Lock()
        self.connected = False
        self.position = {'x': 0, 'y': 0, 'z': 0}
        self.gripper = 'open'
        self.pump = 'off'

    def connect(self):
        """Connect to hardware"""
        try:
            with self.lock:
                if self.ser:
                    self.ser.close()

                self.ser = serial.Serial(
                    self.port, self.baudrate, timeout=self.timeout
                )
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                self.connected = True
                logger.info(f"Connected to {self.port}")
                return True
        except serial.SerialException as e:
            logger.error(f"Connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from hardware"""
        with self.lock:
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.connected = False
            logger.info("Disconnected")

    def _send_command(self, cmd_id, command):
        """Send command and get response"""
        if not self.connected or not self.ser:
            raise Exception("Not connected")

        try:
            self.ser.write(f"#{cmd_id} {command}\n".encode())
            response = self.ser.readline().decode('utf-8').strip()

            if not response.startswith(f"${cmd_id}"):
                raise Exception(f"Invalid response: {response}")

            return response
        except serial.SerialException as e:
            self.connected = False
            raise Exception(f"Serial error: {e}")

    def get_current_position(self):
        """Query current position"""
        if not self.connected:
            return None

        try:
            with self.lock:
                response = self._send_command(1, "P2220")

            # Parse: $1 ok X100 Y50 Z75
            parts = response.split()
            if len(parts) >= 5:
                self.position = {
                    'x': float(parts[2][1:]),
                    'y': float(parts[3][1:]),
                    'z': float(parts[4][1:]),
                }
            return self.position
        except Exception as e:
            logger.error(f"Position query failed: {e}")
            return None

    def move_to_position(self, x, y, z, speed=1000):
        """Move to position"""
        # Validate
        if not (self.WORKSPACE['x_min'] <= x <= self.WORKSPACE['x_max']):
            return {'success': False, 'error': f"X out of range"}
        if not (self.WORKSPACE['y_min'] <= y <= self.WORKSPACE['y_max']):
            return {'success': False, 'error': f"Y out of range"}
        if not (self.WORKSPACE['z_min'] <= z <= self.WORKSPACE['z_max']):
            return {'success': False, 'error': f"Z out of range"}

        # Clamp speed
        speed = min(max(speed, 1), 2000)

        if not self.connected:
            return {'success': False, 'error': 'Not connected'}

        try:
            with self.lock:
                response = self._send_command(1, f"G0 X{x} Y{y} Z{z} F{speed}")

            self.position = {'x': x, 'y': y, 'z': z}
            logger.info(f"Moved to ({x}, {y}, {z})")
            return {'success': True, 'position': self.position}
        except Exception as e:
            logger.error(f"Move failed: {e}")
            return {'success': False, 'error': str(e)}

    def control_gripper(self, action):
        """Control gripper open/close"""
        if not self.connected:
            return {'success': False}

        try:
            v = 1 if action == 'close' else 0
            with self.lock:
                self._send_command(2, f"M2232 V{v}")

            self.gripper = action
            return {'success': True, 'state': action}
        except Exception as e:
            logger.error(f"Gripper failed: {e}")
            return {'success': False}

    def control_pump(self, state):
        """Control pump on/off"""
        if not self.connected:
            return {'success': False}

        try:
            with self.lock:
                self._send_command(3, f"M2231 V{state}")

            self.pump = 'on' if state else 'off'
            return {'success': True, 'state': state}
        except Exception as e:
            logger.error(f"Pump failed: {e}")
            return {'success': False}

    def emergency_stop(self):
        """Emergency stop"""
        if not self.connected:
            return {'status': 'STOPPED'}

        try:
            with self.lock:
                self._send_command(99, "M2019")

            logger.critical("EMERGENCY STOP")
            return {'status': 'STOPPED'}
        except Exception as e:
            logger.critical(f"E-stop error: {e}")
            return {'status': 'STOPPED'}
