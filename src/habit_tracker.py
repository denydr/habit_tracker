import logging
from src.habit import Habit

# Setting the logger
logger = logging.getLogger("Habit Tracker Logger")
logger.setLevel(logging.INFO)
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter(
     fmt="%(asctime)s - %(module)s - line %(lineno)d - %(levelname)s - %(message)s",
     datefmt="%Y-%m-%d %H:%M:%S"
)
logger.addHandler(logger_console_handler)


class HabitTracker:
    """
    Main class for tracking habits.

    This class provides methods for adding, completing, analyzing and deleting habits.
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

        try:
            habit = Habit(name, description, periodicity)
            habit.id = self.db.save_habit(habit)
            self.habits = self.db.load_habits()
            return habit
        except Exception as e:
            logger.error(f"Task failed for adding a habit: {e}", exc_info=True)

    def complete_habit(self, habit_id):
        """
        Mark a habit as completed.

        Args:
            habit_id (int): The ID of the habit to be completed.

        Returns:
            Habit: The completed habit object, or None if not found.
        """

        try:
            habit = self.get_habit_by_id(habit_id)
            if habit:
                habit.complete_task()
                self.db.update_habit(habit)
            return habit
        except Exception as e:
            logger.error(f"Task failed for completing a habit: {e}", exc_info=True)

    def get_habit_by_id(self, habit_id):
        """
        Get a habit by its ID.

        Args:
            habit_id (int): The ID of the habit to retrieve.

        Returns:
            Habit: The habit object with the given ID, or None if not found.
        """

        # This statement - (habit for habit in self.habits if habit.id == habit_id) - returns the iterator
        # object but not the habit object itself.
        # Therefore, next function is needed to return the actual habit object from the iterator.
        try:
            return next((habit for habit in self.habits if habit.id == habit_id), None)
        except Exception as e:
            logger.error(f"Task failed for getting a habit by ID: {e}", exc_info=True)

    def get_all_habits(self):
        """
        Get all habits.

        Returns:
            list: A list of all Habit objects.
        """

        try:
            return self.habits
        except Exception as e:
            logger.error(f"Get all habits failed: {e}", exc_info=True)

    def get_habits_by_periodicity(self, periodicity):
        """
        Get habits by their periodicity.

        Args:
            periodicity (str): The periodicity to filter by ('daily' or 'weekly').

        Returns:
            list: A list of Habit objects with the given periodicity.
        """

        try:
            return [habit for habit in self.habits if habit.periodicity == periodicity]
        except Exception as e:
            logger.error(f"Get habits by periodicity failed, {e}", exc_info=True)

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
        try:
            for habit in self.habits:
                streak = habit.get_accumulated_streak()
                if streak > longest_streak:
                    longest_streak = streak
                    longest_streak_habit = habit
        except Exception as e:
            logger.error(f"Get longest streak for all habits failed, {e}", exc_info=True)

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

        try:
            return habit.get_accumulated_streak()
        except Exception as e:
            logger.error(f"Get longest streak for given habit failed, {e}", exc_info=True)

    def delete_habit(self, habit_id):
        """
        Delete a habit.

        Args:
            habit_id (int): The ID of the habit to be deleted.

        Returns:
            Habit: The deleted habit object, or None if not found.
        """

        try:
            habit = self.get_habit_by_id(habit_id)
            if habit:
                self.db.delete_habit(habit_id)
                self.habits = self.db.load_habits()
            return habit
        except Exception as e:
            logger.error(f"Deleting habit_id={habit_id} failed, {e}", exc_info=True)
