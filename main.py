"""Entry point"""
from app import create_app
from backend.arm_controller import SwiftArmController

if __name__ == '__main__':
    controller = SwiftArmController('/dev/ttyUSB0')
    controller.connect()

    app = create_app('production', arm_controller=controller)
    app.run(host='0.0.0.0', port=5000, debug=False)
