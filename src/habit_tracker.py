from src.habit import Habit

# TODO: Add error handling (try...except)
# TODO: Implement logging
class HabitTracker:
    """
    Main class for tracking habits.

    This class provides methods for adding, completing, and analyzing habits.
    It uses a DataPersistence object to interact with the database.
    """

    def __init__(self, db):
        """
        Initialize the HabitTracker.

        Args:
            db (DataPersistence): A DataPersistence object for database operations.
        """
        self.db = db
        self.habits = self.db.load_habits()

    def add_habit(self, name, description, periodicity):
        """
        Add a new habit.

        Args:
            name (str): Name of the habit.
            description (str): Description of the habit.
            periodicity (str): Frequency of the habit ('daily' or 'weekly').

        Returns:
            Habit: The newly created habit object.
        """
        habit = Habit(name, description, periodicity)
        habit.id = self.db.save_habit(habit)
        self.habits.append(habit)
        return habit

    def complete_habit(self, habit_id):
        """
        Mark a habit as completed.

        Args:
            habit_id (int): The ID of the habit to be completed.

        Returns:
            Habit: The completed habit object, or None if not found.
        """
        habit = self.get_habit_by_id(habit_id)
        if habit:
            habit.complete_task()
            self.db.update_habit(habit)
        return habit

    def get_habit_by_id(self, habit_id):
        """
        Get a habit by its ID.

        Args:
            habit_id (int): The ID of the habit to retrieve.

        Returns:
            Habit: The habit object with the given ID, or None if not found.
        """
        return next((habit for habit in self.habits if habit.id == habit_id), None)

    def get_all_habits(self):
        """
        Get all habits.

        Returns:
            list: A list of all Habit objects.
        """
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        """
        Get habits by their periodicity.

        Args:
            periodicity (str): The periodicity to filter by ('daily' or 'weekly').

        Returns:
            list: A list of Habit objects with the given periodicity.
        """
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_longest_streak_all_habits(self):
        """
        Get the longest streak across all habits.

        Returns:
            tuple: A tuple containing the longest streak (int) and the corresponding Habit object.
        """
        if not self.habits:
            return 0, None
        longest_streak = 0
        longest_streak_habit = None
        for habit in self.habits:
            streak = habit.get_current_streak()
            if streak > longest_streak:
                longest_streak = streak
                longest_streak_habit = habit
        return longest_streak, longest_streak_habit

    @staticmethod
    def get_longest_streak_for_habit(habit):
        """
        Get the longest streak for a specific habit.

        Args:
            habit (Habit): The habit to analyze.

        Returns:
            int: The longest streak for the given habit.
        """
        return habit.get_current_streak()

    def delete_habit(self, habit_id):
        """
        Delete a habit.

        Args:
            habit_id (int): The ID of the habit to be deleted.

        Returns:
            Habit: The deleted habit object, or None if not found.
        """
        habit = self.get_habit_by_id(habit_id)
        if habit:
            self.db.delete_habit(habit_id)
        return habit

