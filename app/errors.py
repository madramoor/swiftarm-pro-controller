"""Custom exceptions"""


class ArmControllerError(Exception):
    """Base exception"""
    def __init__(self, message, code=500, user_message=None):
        self.message = message
        self.code = code
        self.user_message = user_message or message
        super().__init__(self.message)


class PositionOutOfBounds(ArmControllerError):
    def __init__(self, x, y, z):
        msg = f"Position ({x}, {y}, {z}) out of bounds"
        super().__init__(msg, 400, msg)


class ArmNotConnected(ArmControllerError):
    def __init__(self):
        super().__init__("Arm not connected", 503, "Arm not connected")


class SerialTimeout(ArmControllerError):
    def __init__(self):
        super().__init__("Serial timeout", 504, "Communication timeout")


class InvalidSpeed(ArmControllerError):
    def __init__(self, speed):
        msg = f"Speed {speed} invalid (1-2000)"
        super().__init__(msg, 400, msg)
