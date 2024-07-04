from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
from src.data_persistence import DataPersistence
from src.habit import Habit
import os

# Load environment variables from .env file
load_dotenv()

# Setting the logger
logger = logging.getLogger("Sample Data Logger")
logger.setLevel(logging.INFO)
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter(
     fmt="%(asctime)s - %(module)s - line %(lineno)d - %(levelname)s - %(message)s",
     datefmt="%Y-%m-%d %H:%M:%S"
)
logger.addHandler(logger_console_handler)


class SampleDataGenerator:
    """ Sample data generator class """

    @staticmethod
    def generate_sample_data(db):
        """
        Generate and insert sample data into the database.

        Args:
            db (DataPersistence): The database connection object.
        """
        try:
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
        except Exception as e:
            db.conn.rollback()
            logger.error(f"Fail to generate and insert the sample data into the db, {e}", exc_info=True)
        finally:
            if db.cur:
                db.cur.close()
            if db.conn:
                db.conn.close()


if __name__ == "__main__":

    sdg = SampleDataGenerator()

    dbname = os.getenv("DATABASE_NAME"),
    user = os.getenv("DATABASE_USER"),
    password = os.getenv("DATABASE_PASSWORD"),
    host = os.getenv("DATABASE_HOST"),
    port = int(os.getenv("DATABASE_PORT"))

    # Update these with your actual database credentials
    db_obj = DataPersistence(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    sdg.generate_sample_data(db_obj)
