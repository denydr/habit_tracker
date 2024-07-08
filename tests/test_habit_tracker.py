from datetime import datetime, timedelta
import os
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.habit_tracker import HabitTracker   # noqa:
from src.habit import Habit  # noqa:


class MockDataPersistence:
    """
    Class for testing data persistence.
    This class simulates the behavior of the DataPersistence class,
    allowing for testing without a real database.
    """

    def __init__(self):
        """
        Initialize the MockDataPersistence.
        Creates an empty list to store habits.
        """

        self.habits = []

    def save_habit(self, habit):
        """
        Save a habit.

        Args:
            habit (Habit): The habit object to be saved.

        Returns:
            int: The ID of the saved habit.
        """

        if not any(h.id == habit.id for h in self.habits):
            habit.id = len(self.habits) + 1
            self.habits.append(habit)
        return habit.id

    def load_habits(self):
        """
        Load all habits.

        Returns:
                list: A copy of the list of all habit objects.
        """

        return self.habits.copy()

    def update_habit(self, habit):
        """
        Update a habit.

        Args:
            habit (Habit): The habit object with updated data.
        """

        for i, h in enumerate(self.habits):
            if h.id == habit.id:
                self.habits[i] = habit
                break

    def delete_habit(self, habit_id):
        """
        Delete a habit.

        Args:
            habit_id (int): The ID of the habit to be deleted.
        """

        self.habits = [h for h in self.habits if h.id != habit_id]


@pytest.fixture
def mock_db():
    """
    Pytest fixture for creating a mock database instance.

    Returns:
            MockDataPersistence: An instance of the mock data persistence class.
    """

    return MockDataPersistence()


@pytest.fixture
def habit_tracker(mock_db):
    """
    Pytest fixture for creating a HabitTracker instance with a mock database.

    Args:
        mock_db (MockDataPersistence): The mock data persistence instance.

    Returns:
        HabitTracker: An instance of the HabitTracker class.
    """

    return HabitTracker(mock_db)


def test_add_habit(habit_tracker):
    """
    Test adding a new habit to the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The habit is added successfully with the correct attributes,
        and the total number of habits in the tracker is as expected.
    """

    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert habit.id == 1
    assert habit.name == "Exercise"
    assert habit.description == "Do 30 minutes of exercise"
    assert habit.periodicity == "daily"
    assert len(habit_tracker.habits) == 1


def test_complete_habit(habit_tracker):
    """
    Test completing a habit in the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The habit is marked as completed and the completion date is recorded.
    """

    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    completed_habit = habit_tracker.complete_habit(habit.id)
    assert completed_habit.is_task_completed()
    assert len(completed_habit.completed_dates) == 1


def test_get_habit_by_id(habit_tracker):
    """
    Test retrieving a habit by its ID from the HabitTracker.

    Args:
         habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
       The habit is retrieved correctly by its ID.
       Returns None for a non-existent habit ID.
    """

    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    habit2 = habit_tracker.add_habit("Read", "Read for 30 minutes", "daily")

    assert habit_tracker.get_habit_by_id(habit1.id) == habit1
    assert habit_tracker.get_habit_by_id(habit2.id) == habit2
    assert habit_tracker.get_habit_by_id(999) is None


def test_get_all_habits(habit_tracker):
    """
    Test retrieving all habits from the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        All habits added to the tracker are retrieved correctly.
    """

    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    habit2 = habit_tracker.add_habit("Read", "Read for 30 minutes", "daily")

    all_habits = habit_tracker.get_all_habits()
    assert len(all_habits) == 2
    assert habit1 in all_habits
    assert habit2 in all_habits


def test_get_habits_by_periodicity(habit_tracker):
    """
    Test retrieving habits by their periodicity from the HabitTracker.

    Args:
         habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        Habits are correctly filtered and retrieved by their periodicity.
    """

    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    habit2 = habit_tracker.add_habit("Read", "Read for 30 minutes", "daily")
    habit3 = habit_tracker.add_habit("Clean", "Clean the house", "weekly")

    daily_habits = habit_tracker.get_habits_by_periodicity("daily")
    weekly_habits = habit_tracker.get_habits_by_periodicity("weekly")

    assert len(daily_habits) == 2
    assert habit1 in daily_habits
    assert habit2 in daily_habits
    assert len(weekly_habits) == 1
    assert habit3 in weekly_habits


def test_get_longest_streak_all_habits(habit_tracker):
    """
    Test retrieving the longest streak across all habits in the HabitTracker.

    Args:
         habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
       The longest streak and corresponding habit are correctly identified.
    """

    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    habit2 = habit_tracker.add_habit("Read", "Read for 30 minutes", "daily")

    # Complete habit1 for 3 days
    for _ in range(3):
        habit_tracker.complete_habit(habit1.id)
        habit1.creation_date -= timedelta(days=1)

    # Complete habit2 for 5 days
    for _ in range(5):
        habit_tracker.complete_habit(habit2.id)
        habit2.creation_date -= timedelta(days=1)

    longest_streak, longest_streak_habit = habit_tracker.get_longest_streak_all_habits()
    assert longest_streak == 5
    assert longest_streak_habit == habit2


def test_get_longest_streak_for_habit(habit_tracker):
    """
    Test retrieving the longest streak for a specific habit in the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The longest streak for the specified habit is correctly identified.
    """

    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")

    # Complete habit for 3 days
    for _ in range(3):
        habit_tracker.complete_habit(habit.id)
        habit.creation_date -= timedelta(days=1)

    longest_streak = habit_tracker.get_longest_streak_for_habit(habit)
    assert longest_streak == 3


def test_habit_is_task_completed(habit_tracker):
    """
    Test checking if a task is completed for a habit in the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The task completion status of a habit is correctly identified.
    """

    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    if not habit.is_task_completed():
        assert not habit.is_task_completed()
    else:
        habit_tracker.complete_habit(habit.id)
        assert habit.is_task_completed()

    # Set completion date to yesterday
    habit.completed_dates[-1] = datetime.now() - timedelta(days=1)
    assert not habit.is_task_completed()


def test_habit_get_accumulated_streak(habit_tracker):
    """
    Test getting the accumulated streak for a habit in the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The accumulated streak for a habit is correctly calculated.
    """

    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert habit.get_accumulated_streak() == 0

    # Complete habit for 3 consecutive days
    for _ in range(3):
        habit_tracker.complete_habit(habit.id)
        habit.creation_date -= timedelta(days=1)

    assert habit.get_accumulated_streak() == 3


def test_delete_habit_success(habit_tracker):
    """
    Test deleting an existing habit from the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The habit is deleted successfully and is no longer present in the list of habits.
    """

    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert len(habit_tracker.habits) == 1

    deleted_habit = habit_tracker.delete_habit(habit.id)
    assert deleted_habit == habit
    assert len(habit_tracker.habits) == 0
    assert habit_tracker.get_habit_by_id(habit.id) is None


def test_delete_habit_not_found(habit_tracker):
    """
    Test attempting to delete a habit that does not exist in the HabitTracker.

    Args:
        habit_tracker (HabitTracker): The habit tracker instance to use for the test.

    Asserts:
        The method returns None and no habits are deleted.
    """

    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert len(habit_tracker.habits) == 1

    deleted_habit = habit_tracker.delete_habit(999)
    assert deleted_habit is None
    assert len(habit_tracker.habits) == 1
    assert habit_tracker.get_habit_by_id(habit1.id) == habit1

# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
