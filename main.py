"""Entry point with COM11 configuration"""
import os
from flask import Flask
from app import create_app
from backend.arm_controller import SwiftArmController
from backend.mock_controller import MockArmController

if __name__ == '__main__':
    # Create controller on COM11
    controller = SwiftArmController('COM11')
    try:
        result = controller.connect()
        if result:
            print("✅ Successfully connected to SwiftArm Pro on COM11")
        else:
            print("❌ Failed to connect. Using mock controller.")
            controller = MockArmController()
    except Exception as e:
        print(f"❌ Connection error: {e}")
        controller = MockArmController()
    
    # Create Flask app
    app = create_app('production', arm_controller=controller)
    
    # Get the directory where main.py is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WEB_DIR = os.path.join(BASE_DIR, 'web')
    
    # Serve frontend files with UTF-8 encoding
    @app.route('/')
    def index():
        try:
            index_path = os.path.join(WEB_DIR, 'index.html')
            with open(index_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return 'Error: web/index.html not found', 404
    
    @app.route('/styles.css')
    def styles():
        try:
            css_path = os.path.join(WEB_DIR, 'styles.css')
            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'text/css'}
        except FileNotFoundError:
            return '', 200, {'Content-Type': 'text/css'}
    
    @app.route('/script.js')
    def script():
        try:
            js_path = os.path.join(WEB_DIR, 'script.js')
            with open(js_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'application/javascript'}
        except FileNotFoundError:
            return '', 200, {'Content-Type': 'application/javascript'}
    
    print(f"Web directory: {WEB_DIR}")
    print(f"Starting server on http://0.0.0.0:5000")
    print(f"Using controller: {type(controller).__name__}")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
