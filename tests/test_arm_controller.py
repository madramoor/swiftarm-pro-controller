"""Hardware controller tests"""
import pytest


def test_mock_connect(mock_controller):
    """Test connect"""
    assert mock_controller.connect() == True
    assert mock_controller.connected == True


def test_mock_disconnect(mock_controller):
    """Test disconnect"""
    mock_controller.connect()
    mock_controller.disconnect()
    assert mock_controller.connected == False


def test_mock_get_position(mock_controller):
    """Test get position"""
    pos = mock_controller.get_current_position()
    assert pos is not None
    assert 'x' in pos
    assert 'y' in pos
    assert 'z' in pos


def test_mock_move_valid(mock_controller):
    """Test valid move"""
    result = mock_controller.move_to_position(100, 0, 50)
    assert result['success'] == True
    assert result['position']['x'] == 100
    assert result['position']['y'] == 0
    assert result['position']['z'] == 50


def test_mock_move_updates_position(mock_controller):
    """Test move updates internal position"""
    mock_controller.move_to_position(150, 75, 100)
    pos = mock_controller.get_current_position()
    assert pos['x'] == 150
    assert pos['y'] == 75
    assert pos['z'] == 100


def test_mock_move_out_of_bounds_x(mock_controller):
    """Test move x out of bounds"""
    result = mock_controller.move_to_position(400, 0, 50)
    assert result['success'] == False
    assert 'error' in result


def test_mock_move_out_of_bounds_y(mock_controller):
    """Test move y out of bounds"""
    result = mock_controller.move_to_position(100, 300, 50)
    assert result['success'] == False


def test_mock_move_out_of_bounds_z(mock_controller):
    """Test move z out of bounds"""
    result = mock_controller.move_to_position(100, 0, 200)
    assert result['success'] == False


def test_mock_move_when_disconnected(mock_controller):
    """Test move when disconnected"""
    mock_controller.disconnect()
    result = mock_controller.move_to_position(100, 0, 50)
    assert result['success'] == False


def test_mock_gripper_open(mock_controller):
    """Test gripper open"""
    result = mock_controller.control_gripper('open')
    assert result['success'] == True
    assert result['state'] == 'open'


def test_mock_gripper_close(mock_controller):
    """Test gripper close"""
    result = mock_controller.control_gripper('close')
    assert result['success'] == True
    assert result['state'] == 'close'


def test_mock_gripper_when_disconnected(mock_controller):
    """Test gripper when disconnected"""
    mock_controller.disconnect()
    result = mock_controller.control_gripper('open')
    assert result['success'] == False


def test_mock_pump_on(mock_controller):
    """Test pump on"""
    result = mock_controller.control_pump(1)
    assert result['success'] == True
    assert result['state'] == 1


def test_mock_pump_off(mock_controller):
    """Test pump off"""
    result = mock_controller.control_pump(0)
    assert result['success'] == True
    assert result['state'] == 0


def test_mock_pump_when_disconnected(mock_controller):
    """Test pump when disconnected"""
    mock_controller.disconnect()
    result = mock_controller.control_pump(1)
    assert result['success'] == False


def test_mock_emergency_stop(mock_controller):
    """Test emergency stop"""
    result = mock_controller.emergency_stop()
    assert result['status'] == 'STOPPED'


def test_mock_move_count_increment(mock_controller):
    """Test move counter increments"""
    assert mock_controller.move_count == 0
    mock_controller.move_to_position(100, 0, 50)
    assert mock_controller.move_count == 1
    mock_controller.move_to_position(150, 50, 75)
    assert mock_controller.move_count == 2


def test_workspace_boundaries(mock_controller):
    """Test all workspace boundaries"""
    # Valid boundaries
    result = mock_controller.move_to_position(50, -200, 0)
    assert result['success'] == True
    
    result = mock_controller.move_to_position(320, 200, 150)
    assert result['success'] == True
    
    # Just outside boundaries
    result = mock_controller.move_to_position(49, 0, 0)
    assert result['success'] == False
    
    result = mock_controller.move_to_position(321, 0, 0)
    assert result['success'] == False
