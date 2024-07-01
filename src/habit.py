from datetime import datetime

# TODO: Add error handling (try...except)
# TODO: Implement logging
class Habit:
    """
    Represents a habit to be tracked.

    Attributes:
        id (int): Unique identifier for the habit.
        name (str): Name of the habit.
        description (str): Detailed description of the habit.
        periodicity (str): Frequency of the habit ('daily' or 'weekly').
        creation_date (datetime): Date and time when the habit was created.
        completed_dates (list): List of datetime objects representing completion dates.
        is_broken (bool): Status indicating if the habit is broken.
    """

    def __init__(self, name, description, periodicity, id=None, creation_date=None):
        """
        Initialize a new Habit object.

        Args:
            name (str): Name of the habit.
            description (str): Detailed description of the habit.
            periodicity (str): Frequency of the habit ('daily' or 'weekly').
            id (int, optional): Unique identifier for the habit. Defaults to None.
            creation_date (datetime, optional): Date and time when the habit was created. Defaults to current time.
        """

        self.id = id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now()  # takes the argument which is not 'None'
        self.completed_dates = []
        self.is_broken = False

    def complete_task(self):
        """Mark the habit as completed for the current date and time."""

        self.completed_dates.append(datetime.now())
        self.is_broken = False

    def is_task_completed(self):
        """
        Check if the habit has been completed within its periodicity.

        Returns:
            bool: True if the habit is completed within its periodicity, False otherwise.
        """

        if not self.completed_dates:
            # If there are no completion dates, check if the habit should have been completed by now
            if self.periodicity == 'daily':
                return (datetime.now() - self.creation_date).days < 1
            elif self.periodicity == 'weekly':
                return (datetime.now() - self.creation_date).days < 7
        else:
            # Check if the last completion date is within the required period
            last_completion = self.completed_dates[-1]
            if self.periodicity == 'daily':
                return (datetime.now() - last_completion).days < 1
            elif self.periodicity == 'weekly':
                return (datetime.now() - last_completion).days < 7

        return False

    def check_if_broken(self):
        """
        Check if the habit has been broken by not being completed within the defined period.

        Returns:
            bool: True if the habit is broken, False otherwise.
        """

        if not self.completed_dates:
            if self.periodicity == 'daily' and (datetime.now() - self.creation_date).days >= 1:
                self.is_broken = True
            elif self.periodicity == 'weekly' and (datetime.now() - self.creation_date).days >= 7:
                self.is_broken = True
            else:
                self.is_broken = False
        else:
            last_completion = self.completed_dates[-1]
            if self.periodicity == 'daily' and (datetime.now() - last_completion).days >= 1:
                self.is_broken = True
            elif self.periodicity == 'weekly' and (datetime.now() - last_completion).days >= 7:
                self.is_broken = True
            else:
                self.is_broken = False

        return self.is_broken

    def get_accumulated_streak(self):
        """
        Calculate the accumulated streak of completed habits.

        Returns:
            int: The number of consecutive times the habit has been completed.
        """

        if not self.completed_dates: # returns 0 if self.completed_dates is 'None'
            return 0

        streak = 0 # initializes 'streak' variable
        current_date = datetime.now()
        for completion_date in reversed(self.completed_dates):
            if self.periodicity == 'daily':
                if (current_date - completion_date).days <= 1:
                    streak += 1
                    current_date = completion_date
                else:
                    break
            elif self.periodicity == 'weekly':
                if (current_date - completion_date).days <= 7:
                    streak += 1
                    current_date = completion_date
                else:
                    break
        return streak
