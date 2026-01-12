"""API endpoint tests"""


def test_status_connected(client):
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.json['status'] == 'connected'


def test_move_valid(client):
    response = client.post('/api/move', json={'x': 100, 'y': 0, 'z': 50, 'speed': 1000})
    assert response.status_code == 200
    assert response.json['success'] == True


def test_move_out_of_bounds(client):
    response = client.post('/api/move', json={'x': 400, 'y': 0, 'z': 50})
    assert response.status_code == 400


def test_move_missing_params(client):
    response = client.post('/api/move', json={'x': 100})
    assert response.status_code == 400


def test_gripper_open(client):
    response = client.post('/api/gripper', json={'action': 'open'})
    assert response.status_code == 200
    assert response.json['success'] == True


def test_gripper_close(client):
    response = client.post('/api/gripper', json={'action': 'close'})
    assert response.status_code == 200


def test_pump_on(client):
    response = client.post('/api/pump', json={'state': 1})
    assert response.status_code == 200


def test_emergency_stop(client):
    response = client.post('/api/emergency-stop')
    assert response.status_code == 200


def test_workspace(client):
    response = client.get('/api/workspace')
    assert response.status_code == 200
    assert response.json['x_max'] == 320
