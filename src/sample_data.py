from datetime import datetime, timedelta
from src.data_persistence import DataPersistence
from src.habit import Habit

# TODO: Add error handling (try...except)
# TODO: Implement logging


class SampleDataGenerator:
    """ Sample data generator class """

    @staticmethod
    def generate_sample_data(db):
        """
        Generate and insert sample data into the database.

        Args:
            db (DataPersistence): The database connection object.
        """
        # Sample habits
        habits = [
            Habit("Morning Exercise", "Do 30 minutes of exercise every morning", "daily"),
            Habit("Read a Book", "Read for 30 minutes before bed", "daily"),
            Habit("Meditate", "Meditate for 10 minutes", "daily"),
            Habit("Weekly Planning", "Plan the upcoming week", "weekly"),
            Habit("Learn a New Skill", "Spend 2 hours learning a new skill", "weekly")
        ]

        # Insert habits and generate sample completions
        for habit in habits:
            habit_id = db.save_habit(habit)
            habit.id = habit_id

            # Generate completions for the past 4 weeks
            if habit.periodicity == "daily":
                for i in range(28):
                    if i % 2 == 0:  # Complete every other day
                        completion_date = datetime.now() - timedelta(days=i)
                        db.cur.execute("""
                            INSERT INTO completions (habit_id, completion_date)
                            VALUES (%s, %s)
                        """, (habit_id, completion_date))
            else:  # weekly
                for i in range(4):
                    completion_date = datetime.now() - timedelta(weeks=i)
                    db.cur.execute("""
                        INSERT INTO completions (habit_id, completion_date)
                        VALUES (%s, %s)
                    """, (habit_id, completion_date))

        db.conn.commit()
        print("Sample data has been generated and inserted into the database.")


if __name__ == "__main__":
    sdg = SampleDataGenerator()
    # Update these with your actual database credentials
    db_obj = DataPersistence(dbname="habit_tracker", user="your_username", password="your_password")
    sdg.generate_sample_data(db_obj)
