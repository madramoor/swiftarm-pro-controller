"""Hardware controller tests"""


def test_mock_connect(mock_controller):
    assert mock_controller.connect() == True
    assert mock_controller.connected == True


def test_mock_move(mock_controller):
    result = mock_controller.move_to_position(100, 0, 50)
    assert result['success'] == True
    assert result['position']['x'] == 100


def test_mock_move_out_of_bounds(mock_controller):
    result = mock_controller.move_to_position(400, 0, 50)
    assert result['success'] == False


def test_mock_gripper(mock_controller):
    result = mock_controller.control_gripper('close')
    assert result['success'] == True


def test_mock_position(mock_controller):
    pos = mock_controller.get_current_position()
    assert pos is not None
