"""API endpoint tests"""
import pytest


def test_status_connected(client):
    """Test getting status when connected"""
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.json['status'] == 'connected'


def test_status_fields(client):
    """Test status response has all fields"""
    response = client.get('/api/status')
    data = response.json
    assert 'status' in data
    assert 'position' in data
    assert 'gripper' in data
    assert 'pump' in data
    assert 'timestamp' in data


def test_move_valid(client):
    """Test valid move command"""
    response = client.post('/api/move', json={'x': 100, 'y': 0, 'z': 50, 'speed': 1000})
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['position']['x'] == 100


def test_move_with_default_speed(client):
    """Test move with default speed"""
    response = client.post('/api/move', json={'x': 150, 'y': 50, 'z': 75})
    assert response.status_code == 200
    assert response.json['success'] == True


def test_move_out_of_bounds_x(client):
    """Test move x out of bounds"""
    response = client.post('/api/move', json={'x': 400, 'y': 0, 'z': 50})
    assert response.status_code == 400


def test_move_out_of_bounds_y(client):
    """Test move y out of bounds"""
    response = client.post('/api/move', json={'x': 100, 'y': 300, 'z': 50})
    assert response.status_code == 400


def test_move_out_of_bounds_z(client):
    """Test move z out of bounds"""
    response = client.post('/api/move', json={'x': 100, 'y': 0, 'z': 200})
    assert response.status_code == 400


def test_move_missing_params(client):
    """Test move with missing parameters"""
    response = client.post('/api/move', json={'x': 100})
    assert response.status_code == 400


def test_move_invalid_json(client):
    """Test move with no JSON"""
    response = client.post('/api/move')
    assert response.status_code == 415


def test_move_invalid_types(client):
    """Test move with invalid types"""
    response = client.post('/api/move', json={'x': 'invalid', 'y': 0, 'z': 50})
    assert response.status_code == 400


def test_gripper_open(client):
    """Test gripper open"""
    response = client.post('/api/gripper', json={'action': 'open'})
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['state'] == 'open'


def test_gripper_close(client):
    """Test gripper close"""
    response = client.post('/api/gripper', json={'action': 'close'})
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['state'] == 'close'


def test_gripper_invalid_action(client):
    """Test gripper with invalid action"""
    response = client.post('/api/gripper', json={'action': 'invalid'})
    assert response.status_code == 400


def test_gripper_no_json(client):
    """Test gripper with no JSON"""
    response = client.post('/api/gripper')
    assert response.status_code == 415


def test_pump_on(client):
    """Test pump on"""
    response = client.post('/api/pump', json={'state': 1})
    assert response.status_code == 200
    assert response.json['success'] == True


def test_pump_off(client):
    """Test pump off"""
    response = client.post('/api/pump', json={'state': 0})
    assert response.status_code == 200
    assert response.json['success'] == True


def test_pump_no_json(client):
    """Test pump with no JSON"""
    response = client.post('/api/pump')
    assert response.status_code == 415


def test_emergency_stop(client):
    """Test emergency stop"""
    response = client.post('/api/emergency-stop')
    assert response.status_code == 200
    assert response.json['status'] == 'STOPPED'


def test_workspace(client):
    """Test workspace bounds"""
    response = client.get('/api/workspace')
    assert response.status_code == 200
    assert response.json['x_min'] == 50
    assert response.json['x_max'] == 320
    assert response.json['y_min'] == -200
    assert response.json['y_max'] == 200
    assert response.json['z_min'] == 0
    assert response.json['z_max'] == 150
