import pytest

def filter_by_state(data, state="EXECUTED"):
    return [item for item in data if item.get("state") == state]

@pytest.mark.parametrize(
    "data, state, expected",
    [
        ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}, {"id": 3, "state": "EXECUTED"}], "EXECUTED", [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]),
        ([{"id": 1, "state": "PENDING"}, {"id": 2, "state": "CANCELED"}], "EXECUTED", []),
        ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}], "EXECUTED", [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED"}]),
        ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}, {"id": 3, "state": "EXECUTED"}], "PENDING", [{"id": 2, "state": "PENDING"}]),
        ([], "EXECUTED", []),
        ([{"id": 1, "state": None}, {"id": 2, "state": "EXECUTED"}], "EXECUTED", [{"id": 2, "state": "EXECUTED"}]),
        ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED", "other_key": "value"}], "EXECUTED", [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "EXECUTED", "other_key": "value"}]),
        ([{"id": 1}, {"id": 2, "state": "EXECUTED"}], "EXECUTED", [{"id": 2, "state": "EXECUTED"}]),
        ([{"id": 1, "state": 123}, {"id": 2, "state": "EXECUTED"}], "EXECUTED", [{"id": 2, "state": "EXECUTED"}]),
    ],
)
def test_filter_by_state(data, state, expected):
    assert filter_by_state(data, state) == expected