import pytest
from datetime import datetime, timedelta
from src.habit_tracker import HabitTracker

# TODO: To fix the pytests: 1) The failing ones; 2) Create additional tests; 3) Add documentation for methods
class MockDataPersistence:
    """ Class for testing data persistence """
    def __init__(self):
        self.habits = []

    def save_habit(self, habit):
        habit.id = len(self.habits) + 1
        self.habits.append(habit)
        return habit.id

    def load_habits(self):
        return self.habits

    def update_habit(self, habit):
        for i, h in enumerate(self.habits):
            if h.id == habit.id:
                self.habits[i] = habit
                break

    def delete_habit(self, habit_id):
        self.habits = [h for h in self.habits if h.id != habit_id]


@pytest.fixture
def mock_db():
    return MockDataPersistence()


@pytest.fixture
def habit_tracker(mock_db):
    return HabitTracker(mock_db)


def test_add_habit(habit_tracker):
    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert habit.id == 1
    assert habit.name == "Exercise"
    assert habit.description == "Do 30 minutes of exercise"
    assert habit.periodicity == "daily"
    assert len(habit_tracker.habits) == 1


def test_complete_habit(habit_tracker):
    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    completed_habit = habit_tracker.complete_habit(habit.id)
    assert completed_habit.is_task_completed()
    assert len(completed_habit.completed_dates) == 1


def test_get_habit_by_id(habit_tracker):
    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    habit2 = habit_tracker.add_habit("Read", "Read for 30 minutes", "daily")

    assert habit_tracker.get_habit_by_id(habit1.id) == habit1
    assert habit_tracker.get_habit_by_id(habit2.id) == habit2
    assert habit_tracker.get_habit_by_id(999) is None


def test_get_all_habits(habit_tracker):
    habit1 = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    habit2 = habit_tracker.add_habit("Read", "Read for 30 minutes", "daily")

    all_habits = habit_tracker.get_all_habits()
    assert len(all_habits) == 2
    assert habit1 in all_habits
    assert habit2 in all_habits


def test_get_habits_by_periodicity(habit_tracker):
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
    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")

    # Complete habit for 3 days
    for _ in range(3):
        habit_tracker.complete_habit(habit.id)
        habit.creation_date -= timedelta(days=1)

    longest_streak = habit_tracker.get_longest_streak_for_habit(habit)
    assert longest_streak == 3


def test_habit_is_task_completed(habit_tracker):
    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert not habit.is_task_completed()

    habit_tracker.complete_habit(habit.id)
    assert habit.is_task_completed()

    # Set completion date to yesterday
    habit.completed_dates[-1] = datetime.now() - timedelta(days=1)
    assert not habit.is_task_completed()


def test_habit_get_current_streak(habit_tracker):
    habit = habit_tracker.add_habit("Exercise", "Do 30 minutes of exercise", "daily")
    assert habit.get_current_streak() == 0

    # Complete habit for 3 consecutive days
    for _ in range(3):
        habit_tracker.complete_habit(habit.id)
        habit.creation_date -= timedelta(days=1)

    assert habit.get_current_streak() == 3

    # Miss a day
    habit.creation_date -= timedelta(days=1)
    assert habit.get_current_streak() == 0


# Run the tests
if __name__ == "__main__":
    pytest.main([__file__])
