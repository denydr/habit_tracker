from datetime import datetime, timedelta
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.habit import Habit  # noqa:


@pytest.fixture
def habit():
    """
    Pytest fixture for creating a Habit instance.

    Returns:
        Habit: An instance of the Habit class.
    """

    return Habit(name="Exercise", description="Do 30 minutes of exercise", periodicity="daily")


def test_habit_initialization(habit):
    """
    Test the initialization of a new Habit object.

    Args:
        habit (Habit): The habit instance to use for the test.

    Asserts:
        The habit is initialized with the correct attributes.
    """

    assert habit.name == "Exercise"
    assert habit.description == "Do 30 minutes of exercise"
    assert habit.periodicity == "daily"
    assert isinstance(habit.creation_date, datetime)
    assert habit.completed_dates == []


def test_habit_complete_task(habit):
    """
    Test marking a habit as completed.

    Args:
        habit (Habit): The habit instance to use for the test.

    Asserts:
        The habit is marked as completed and the completion date is recorded.
    """

    initial_length = len(habit.completed_dates)
    habit.complete_task()
    assert len(habit.completed_dates) == initial_length + 1


def test_habit_is_task_completed_daily(habit):
    """
    Test checking if a daily habit is completed.

    Args:
        habit (Habit): The habit instance to use for the test.

    Asserts:
        The task completion status of a daily habit is correctly identified.
    """

    if not habit.is_task_completed():
        assert not habit.is_task_completed()
    else:
        habit.complete_task()
        assert habit.is_task_completed()

    # Set completion date to yesterday
    habit.completed_dates[-1] = datetime.now() - timedelta(days=1)
    assert not habit.is_task_completed()


def test_habit_is_task_completed_weekly():
    """
    Test checking if a weekly habit is completed.

    Asserts:
        The task completion status of a weekly habit is correctly identified.
    """

    habit = Habit(name="Clean", description="Clean the house", periodicity="weekly")

    if not habit.is_task_completed():
        assert not habit.is_task_completed()

    else:
        habit.complete_task()
        assert habit.is_task_completed()

    # Set completion date to 8 days ago
    habit.completed_dates[-1] = datetime.now() - timedelta(days=8)
    assert not habit.is_task_completed()  # Should not be completed as a week has passed


def test_habit_get_accumulated_streak(habit):
    """
    Test getting the accumulated streak for a habit.

    Args:
        habit (Habit): The habit instance to use for the test.

    Asserts:
        The accumulated streak for a habit is correctly calculated.
    """

    assert habit.get_accumulated_streak() == 0

    # Complete habit for 3 consecutive days
    for _ in range(3):
        habit.complete_task()
        habit.creation_date -= timedelta(days=1)

    assert habit.get_accumulated_streak() == 3


def test_habit_equality(habit):
    """
    Test the equality comparison for Habit objects.

    Args:
        habit (Habit): The habit instance to use for the test.

    Asserts:
        Two Habit objects with the same ID are considered equal.
    """

    habit2 = Habit(name="Exercise", description="Do 30 minutes of exercise", periodicity="daily", id=habit.id)
    assert habit == habit2


def test_habit_hashing(habit):
    """
    Test the hashing functionality for Habit objects.

    Args:
        habit (Habit): The habit instance to use for the test.

    Asserts:
        The hash of a Habit object is based on its ID.
    """

    habit.id = 1
    habit2 = Habit(name="Exercise", description="Do 30 minutes of exercise", periodicity="daily", id=1)
    assert hash(habit) == hash(habit2)


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
