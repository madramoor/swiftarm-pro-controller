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
        self.move_count = 0
    
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
            msg = f"{command}\n"
            print(f"[SERIAL DEBUG] Command: {command}")
            print(f"[SERIAL DEBUG] Sending: {repr(msg)}")
            
            self.ser.write(msg.encode())
            time.sleep(0.1)
            
            if self.ser.in_waiting:
                response = self.ser.readline().decode('utf-8').strip()
                print(f"[SERIAL DEBUG] Response: {repr(response)}")
            else:
                print(f"[SERIAL DEBUG] No response from robot")
                response = None
            
            return response if response else f"${cmd_id} ok"
        except serial.SerialException as e:
            print(f"[SERIAL DEBUG] SerialException: {e}")
            self.connected = False
            raise Exception(f"Serial error: {e}")
    
    def get_current_position(self):
        """Get current position"""
        return self.position
    
    def move_to_position(self, x, y, z, speed=1000):
        """Move to position"""
        if not (self.WORKSPACE['x_min'] <= x <= self.WORKSPACE['x_max']):
            return {'success': False, 'error': f"X out of range"}
        if not (self.WORKSPACE['y_min'] <= y <= self.WORKSPACE['y_max']):
            return {'success': False, 'error': f"Y out of range"}
        if not (self.WORKSPACE['z_min'] <= z <= self.WORKSPACE['z_max']):
            return {'success': False, 'error': f"Z out of range"}
        
        speed = min(max(speed, 1), 2000)
        
        if not self.connected:
            return {'success': False, 'error': 'Not connected'}
        
        try:
            with self.lock:
                response = self._send_command(1, f"G0 X{x} Y{y} Z{z} F{speed}")
            
            self.position = {'x': float(x), 'y': float(y), 'z': float(z)}
            self.move_count += 1
            return {'success': True, 'position': self.position}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def control_gripper(self, action):
        """Control gripper"""
        if not self.connected:
            return {'success': False}
        
        try:
            with self.lock:
                v = 1 if action == 'close' else 0
                self._send_command(2, f"M2232 V{v}")
            
            self.gripper = action
            return {'success': True, 'state': action}
        except Exception as e:
            return {'success': False}
    
    def control_pump(self, state):
        """Control pump"""
        if not self.connected:
            return {'success': False}
        
        try:
            with self.lock:
                self._send_command(3, f"M2231 V{state}")
            
            self.pump = 'on' if state else 'off'
            return {'success': True, 'state': self.pump}
        except Exception as e:
            return {'success': False}
    
    def emergency_stop(self):
        """Emergency stop"""
        if not self.connected:
            return {'status': 'STOPPED'}
        
        try:
            with self.lock:
                self._send_command(99, "M2019")
            return {'status': 'STOPPED'}
        except Exception as e:
            return {'status': 'STOPPED'}
