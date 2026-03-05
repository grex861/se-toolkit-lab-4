"""Unit tests for interaction filtering edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_multiple_matches_for_same_item_id() -> None:
    """Edge case: multiple interactions with the same item_id should all be returned."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),
        _make_log(3, 3, 2),
        _make_log(4, 1, 1),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert all(log.item_id == 1 for log in result)
    assert set(log.id for log in result) == {1, 2, 4}


def test_filter_returns_empty_when_no_matching_item_id() -> None:
    """Edge case: non-existent item_id should return empty list."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_with_zero_item_id() -> None:
    """Boundary value: item_id of 0 should be handled correctly."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(log.item_id == 0 for log in result)
    assert set(log.id for log in result) == {1, 3}


def test_filter_with_negative_item_id() -> None:
    """Boundary value: negative item_id should be handled correctly."""
    interactions = [
        _make_log(1, 1, -1),
        _make_log(2, 2, 1),
        _make_log(3, 3, -1),
    ]
    result = _filter_by_item_id(interactions, -1)
    assert len(result) == 2
    assert all(log.item_id == -1 for log in result)
    assert set(log.id for log in result) == {1, 3}