"""Unit tests for interaction filtering edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


# KEPT: covers the case where all interactions are above max_item_id, returning empty list
def test_filter_returns_empty_when_all_above_max() -> None:
    """All interactions have item_id greater than max_item_id."""
    interactions = [_make_log(1, 1, 5), _make_log(2, 2, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
    assert result == []


# KEPT: tests boundary case with zero max_item_id
def test_filter_with_zero_max_item_id() -> None:
    """max_item_id is zero, only zero or negative item_ids should pass."""
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1), _make_log(3, 3, -1)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3


# KEPT: tests negative max_item_id boundary case
def test_filter_with_negative_max_item_id() -> None:
    """max_item_id is negative, only more negative or equal item_ids pass."""
    interactions = [_make_log(1, 1, -5), _make_log(2, 2, -3), _make_log(3, 3, -1)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=-3)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


# KEPT: tests negative item_ids with positive max_item_id
def test_filter_with_negative_item_ids() -> None:
    """Interactions have negative item_ids with positive max_item_id."""
    interactions = [_make_log(1, 1, -10), _make_log(2, 2, -5), _make_log(3, 3, 3)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


# KEPT: tests multiple items at exact boundary value
def test_filter_multiple_at_exact_boundary() -> None:
    """Multiple interactions have item_id exactly equal to max_item_id."""
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 5),
        _make_log(3, 3, 5),
        _make_log(4, 4, 6),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert len(result) == 3
    assert all(i.item_id == 5 for i in result)


# KEPT: tests mixed values around boundary comprehensively
def test_filter_mixed_values_around_boundary() -> None:
    """Mix of values below, at, and above max_item_id boundary."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 4),
        _make_log(3, 3, 5),
        _make_log(4, 4, 5),
        _make_log(5, 5, 6),
        _make_log(6, 6, 10),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert len(result) == 4
    assert all(i.item_id <= 5 for i in result)


# KEPT: tests large numbers for overflow edge cases
def test_filter_with_very_large_item_ids() -> None:
    """Interactions have very large item_id values."""
    interactions = [
        _make_log(1, 1, 1_000_000),
        _make_log(2, 2, 999_999),
        _make_log(3, 3, 1_000_001),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=1_000_000)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


# KEPT: tests very large max_item_id includes all interactions
def test_filter_with_very_large_max_item_id() -> None:
    """max_item_id is very large, all interactions should pass."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 100),
        _make_log(3, 3, 10_000),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=1_000_000_000)
    assert result == interactions


# KEPT: tests filtering with duplicate item_ids
def test_filter_with_duplicate_item_ids() -> None:
    """Multiple interactions share the same item_id."""
    interactions = [
        _make_log(1, 1, 3),
        _make_log(2, 2, 3),
        _make_log(3, 3, 3),
        _make_log(4, 4, 5),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
    assert len(result) == 3
    assert all(i.item_id == 3 for i in result)


# KEPT: tests single interaction above max returns empty
def test_filter_single_interaction_above_max() -> None:
    """Single interaction with item_id above max_item_id returns empty."""
    interactions = [_make_log(1, 1, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert result == []


# DISCARDED: would duplicate test_filter_includes_interaction_at_boundary from test_interactions.py
# def test_filter_boundary_value_inclusive_duplicate() -> None:
#     interactions = [_make_log(1, 1, 2)]
#     result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
#     assert len(result) == 1
#     assert result[0].id == 1
